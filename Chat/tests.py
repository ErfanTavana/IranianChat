function
sendSeenMessages(chatId)
{
    const
messagesContainer = document.getElementById('messages-container');
const
messageElements = messagesContainer.querySelectorAll('li[data-message-id]');
const
messageIds = [];

messageElements.forEach(function(messageElement)
{
    const
messageId = messageElement.getAttribute('data-message-id');
const
seen = messageElement.getAttribute('data-seen');

if (seen === "false")
{
    messageIds.push(messageId);
messageElement.setAttribute('data-seen', "true");
}
});
if (messageIds.length > 0) {
$.ajax({
url: '{% url "seen_messages_name" %}',
method: 'POST',
data: {
    chat_id: chatId,
    message_ids: messageIds.join(',')
},
headers: {
    'X-CSRFToken': getCsrfToken()
},
success: function(response)
{
if (response.status === 'success')
{
    console.log('پیام‌ها با موفقیت به عنوان دیده شده علامت‌گذاری شدند.');
} else {
    console.error('خطا در علامت‌گذاری پیام‌ها به عنوان دیده شده:', response.message);
}
},
error: function(xhr, status, error)
{
    console.error('خطا در ارسال درخواست AJAX:', error);
}
});
}
}

// فراخوانی
تابع
هر
5
ثانیه
با
استفاده
از
chatId
const
chatId = '{{ chat_detail.id }}';
setInterval(function()
{
if (document.visibilityState === 'visible')
{
    sendSeenMessages(chatId);
}
}, 2000);