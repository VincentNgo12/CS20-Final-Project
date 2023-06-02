from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="EnigmaFrontPage"),
    path("simulator", views.simulator, name="EnigmaSimulator"),
    path("encryptor", views.encryptor, name="encryptor"),
    path("sendMessage", views.sendMessage, name="sendEncryptedMessage"),
    path("messages/<str:group>", views.viewMessages, name="viewMessages"),
    path("message/<int:messageID>", views.message, name="message"),
    path("message/remove/<int:messageID>", views.removeMessage, name="removeMessage")

]
