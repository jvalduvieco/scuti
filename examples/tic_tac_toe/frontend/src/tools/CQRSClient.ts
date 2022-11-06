import {BACKEND_URL} from "../config";
import {HttpStatus} from "./HttpStatus";

export class CQRSClient {

  static async command(body: string, onError: (response: Response) => void) {
    const response = await fetch(
        `${BACKEND_URL}/commands`, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: body
        }
    );
    if (response.status !== HttpStatus.OK) onError(response)
    return await response.json();
  }

  static async doCommand(type: string, payload: object) {
    const body = JSON.stringify({command: {type, payload}});
    const onError = (response: Response) => {
      throw Error(`${response.status} while performing ${type} command with payload ${payload} (${response.statusText})`);
    }
    return await CQRSClient.command(body, onError);
  }

  static async query(body: string, onError: (response: Response) => void) {
    const response = await fetch(
        `${BACKEND_URL}/queries`, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: body
        }
    );
    if (response.status !== HttpStatus.OK) onError(response);
    return JSON.parse(await response.text());
  }

  static async doQuery(type: string, payload: object) {
    const body = JSON.stringify({query: {type, payload}});
    const onError = (response: Response) => {
      throw Error(`${response.status} while performing ${type} query with payload ${payload} (${response.statusText})`);
    }
    return await CQRSClient.query(body, onError);
  }

  static async event(body: string, onError: (response: Response) => void) {
    const response = await fetch(
        `${BACKEND_URL}/events`, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: body
        }
    );
    if (response.status !== HttpStatus.OK) onError(response)
    return await response.json();
  }

  static async sendEvent(type: string, payload: object) {
    const body = JSON.stringify({event: {type, payload}});
    const onError = (response: Response) => {
      throw Error(`${response.status} while sending ${type} event with payload ${payload} (${response.statusText})`);
    }
    return await CQRSClient.event(body, onError);
  }
}
