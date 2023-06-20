from flask_login import current_user
from flask_socketio import SocketIO, join_room, leave_room, emit
from app import app
from security.authentication import authenticated
import service.userService as userService

socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins=['http://localhost:5173'])
socketio.run(app, allow_unsafe_werkzeug=True)
app.socketio = socketio


@socketio.on('connect')
@authenticated
def test_connect():
    join_room(current_user.id)
    userService.setUsersActiveStatus(current_user.id, True)


@socketio.on('disconnect')
@authenticated
def test_disconnect():
    leave_room(current_user.id)
    userService.setUsersActiveStatus(current_user.id, False)
    emit('session_alive', to=current_user.id)


@socketio.on('alive')
@authenticated
def handle_message():
    userService.setUsersActiveStatus(current_user.id, True)
