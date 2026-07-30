import os
import gradio as gr


def launch_ui(assistant):

    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history

        print("USER SAID:", message)
        reply = assistant.chat(message)
        print("REPLY:", reply)

        chat_history.append(
            {"role": "user", "content": message}
        )

        chat_history.append(
            {"role": "assistant", "content": reply}
        )

        return "", chat_history

    def reset_chat():
        assistant.reset()
        return []

    with gr.Blocks() as demo:

        gr.Markdown("# 🤖 AI Personal Assistant")

        chatbot = gr.Chatbot(
            label="Conversation"
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type a message...",
                scale=5
            )

            submit_btn = gr.Button(
                "Send",
                scale=1
            )

        clear_btn = gr.Button("Clear Chat")

        submit_btn.click(
            respond,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )

        msg.submit(
            respond,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )

        clear_btn.click(
            reset_chat,
            outputs=chatbot
        )

    # ==========================================
    # Launch for Local PC and Render
    # ==========================================

    render_port = os.environ.get("PORT")

    if render_port:
        # Running on Render
        demo.launch(
            server_name="0.0.0.0",
            server_port=int(render_port),
            inbrowser=False,
            quiet=True
        )
    else:
        # Running locally
        demo.launch(
            server_name="127.0.0.1",
            server_port=7861,
            inbrowser=True,
            quiet=True
        )