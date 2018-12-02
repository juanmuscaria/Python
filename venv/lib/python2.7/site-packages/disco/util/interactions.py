

class Dialog(object):
    pass


"""
dialog = Dialog(user)
dialog = Dialog(user, channel=channel)
dialog = Dialog([users ...], channel=channel)


# Basic Dialog
dialog = Dialog(user)
dialog.send('Hey there, please input a message to send: ')
message = dialog.wait_for_input(timeout=60)
result = dialog.confirm('Ok, are you sure?', yes=YES_EMOJI, no=NO_EMOJI)
if not result:
    dialog.send('Ok, cancelling...')
else:
    do_something_with_message(message)
"""
