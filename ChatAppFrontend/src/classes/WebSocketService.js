import { io } from 'socket.io-client'

export class WebSocketService {
  constructor(appContext, handleMessageFromWS, websocketUrl) {
    this.websocketUrl = websocketUrl
    this.handleMessageFromWS = handleMessageFromWS
    for (const property in appContext) {
      this[property] = appContext[property]
    }
  }

  establishStompConnection() {
    this.socket = io('localhost:5000', {
      extraHeaders: {
        Authorization: `Bearer ${this.jwt}`
      }
    });
    this.socket.on('session_alive', () => {
      this.socket.emit('alive');
    });

    this.socket.on('message', (res) => {
      const wsMessage = res.data
      this.handleMessageFromWS(wsMessage)
    });
  }

  closeStompConnection() {
    this.socket.disconnect();
  }
}
