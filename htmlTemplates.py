css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://assets-global.website-files.com/6426543485efe6a5ade36f21/64351f58d7ef3c6b6bfac441_AI_Generated-_a_portrait_of_a_doctor_in_a_stethoscope_in_the_style_of_-92-image_ghost-medical_ghost-productions.webp" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
# https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://images.newscientist.com/wp-content/uploads/2019/06/15113802/what-is-the-body-made-of-p6n94r_web.jpg?width=1200">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
