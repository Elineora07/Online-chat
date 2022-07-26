from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

import asyncio

chat_msgs = []
online_users = set()

MAX_MESSAGES_COUNT = 100

async def main():
	global chat_msgs

	put_markdown("Assalom-u Aleykum, Bizni onlayn chatimizga xush kelibsiz!")

	msg_box = output()
	put_scrollable(msg_box, height=100, keep_button=True)

	nickname = await input("Chatga kirish", required=True, placeholder="Sizni ismingiz", validate=lambda n: "Bu ism avvaldan mavjud!" if n in online_users or n == "🔊" else None)
	online_users.add(nickname)


	chat_msgs.append(('🔊', f"'{nickname}' Chatga qo'shildi!"))
	msg_box.append(put_markdown(f"'{nickname}' Chatga qo'shildi!"))


	refresh_task = run_async(refresh_msg(nickname, msg_box))


	while True:
		data = await input_group("Yangi xabar!",[
			input(placeholder="Xabar matni", name='msg'),
			actions(name='cmd', buttons=['Yuborish', {'label':'chatdan chiqish', 'type':'cancel'}])

		], validate=lambda n: ('msg', "Xabar matini kiriting") if n['cmd'] == "Yuborish" and not n['msg'] else None)

		if data is None:
			break


		msg_box.append(put_markdown(f"'{nickname}': {data['msg']}"))
		chat_msgs.append((nickname, data['msg']))


	# exit chat
	refresh_task.close()

	online_users.remove(nickname)
	toast("Siz chatni tark etdingiz!")
	msg_box.append(put_markdown(f"🔊 Foydalanuchi '{nickname}' chatni tark etdi"))
	chat_msgs.append('🔊',f"Foydalanuchi '{nickname}' chatni tark etdi")

	put_buttons(["Qayta kirish"], onclick=lambda btn: run_js('window.location.reload('))



async def refresh_msg(nickname, msg_box):
	global chat_msgs

	last_idx = len(chat_msgs)

	while True:
		await asyncio.sleep(1)


		for n in chat_msgs[last_idx:]:
			if n[0] != nickname:
				msg_box.append(put_markdown(f"'{n[0]}': {n[1]}"))


		# remove
		if len(chat_msgs) > MAX_MESSAGES_COUNT:
			chat_msgs = chat_msgs[len(chat_msgs) // 2:]


		last_idx = len(chat_msgs)


if __name__ == '__main__':
	start_server(main, debug=True, port=8080, cdn=False)