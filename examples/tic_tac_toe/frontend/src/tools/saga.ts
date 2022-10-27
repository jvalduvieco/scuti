import {Action} from 'redux';

export function sagaErrorHandler<T extends Action>(lambda: (action: T) => Generator,
                                                   rollback: (action: T) => Generator | void = (_: T) => {}) {
  return function* (action: T) {
    try {
      yield lambda(action)
    } catch (error) {
      yield rollback(action)
    }
  }
}
