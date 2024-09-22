# lets import graphical user interface 
import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS 
from langchain.memory import ConversationBufferMemory
#from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain # to chat with our vector store 
from htmlTemplates import css, bot_template, user_template


 




def get_pdf_text(pdf_docs):

    text = ""  # empty variable 

    # To create pages of pdf 
    for pdf in pdf_docs: # we loop one pdf doc at a time from all the list of pdf's
        pdf_reader = PdfReader(pdf) ## intializing one pdf reader object for one pdf 
        for page in pdf_reader.pages: ## we are looping through every page of taken pdf 
            text += page.extract_text()  # we are appending all the content to the pdf file (which is intialized one at a time) to text(variable)
    return text # single string with raw content 

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap= 200,
        length_function = len
        )
        # seperator="\n",
        # chunk_size = 1000,
        # chunk_overlap= 200,
        # length_function = len) # creating new instance (text_splitter)
    chunks = text_splitter.split_text(text)
    
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")


    vectorstore = FAISS.from_texts(texts= text_chunks, embedding = embeddings)
    # store to db
    vectorstore.save_local("faiss_index")
    new_db = FAISS.load_local("faiss_index", embeddings)
    return new_db

def get_conversation_chain(new_db):
    llm = ChatOpenAI() # replace it with hugging face models instead of openAI
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages = True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = new_db.as_retriever(),
        memory = memory 

    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    #st.write(response)
    st.session_state.chat_history =  response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html = True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html = True)    
    

    






def main():
    load_dotenv()
    st.set_page_config(page_title="Friend_Online_doctor", page_icon =":male-doctor:")
    st.write(css, unsafe_allow_html= True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Your online doctor is here")
    user_question = st.text_input("ask me your doubts? ")
    if user_question:
        handle_userinput(user_question)
    #st.write(css, unsafe_allow_html= True)
    # st.write(user_template.replace("{{MSG}}", "Hello_Doctor"), unsafe_allow_html = True) # to tell streamlit to show html message inside of it 
    # st.write(bot_template.replace("{{MSG}}", "HEY PATIENT"), unsafe_allow_html = True )


    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your documents", accept_multiple_files= True)
        if st.button("process"):
            with st.spinner("processing"):

             # get pdf text from the pdfs 
                raw_text = get_pdf_text(pdf_docs)
                #st.write(raw_text) # everyting sentence in all the pdf's is stored in a single variable called raw_text


                # get text chunks 
            
                text_chunks = get_text_chunks(raw_text)
                #st.write(text_chunks)
                
                # create vector embeddings store
                #new_db = FAISS.load_local("faiss_index", embeddings)
                # if new_db == None:
                new_db = get_vectorstore(text_chunks)
                #vectorstore = get_vectorstore(text_chunks)

                # create an instance of conversation chain 
                st.session_state.conversation = get_conversation_chain(new_db) # session state to make above variables persistant 


    #st.session_state.conversation  # using it outside of scope 

    





if __name__ == '__main__':
    main()

    





