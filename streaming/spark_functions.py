def send_via_socket(sid):
    def _send_via_socket(*args, **kwargs):
        return sid
        # socketio.emit('dashboard.status-create', data=data, room=self.sid)  # TODO remove
    return _send_via_socket
