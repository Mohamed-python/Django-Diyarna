def get_bot_reply(message):
    message = message.lower()

    if "سلام" in message or "hello" in message:
        return "أهلًا بيك 👋 تحب أساعدك في إيه؟"
    # elif "سعر" in message:
    #     return "من فضلك قولي اسم الخدمة أو المنتج."
    elif "شكرا" in message or "thanks" in message:
        return "العفو 🌸 لو محتاج أي حاجة أنا موجود."
    # elif "موقع" in message:
    #     # مثال على رد بلينك
    #     return 'زور الموقع الرسمي هنا: <a href="https://chatgpt.com/" target="_blank">https://chatgpt.com/</a>'
    else:
        return "مش فاهمك قوي 😅 ممكن توضح أكتر؟"

