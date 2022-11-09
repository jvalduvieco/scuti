import "@testing-library/jest-dom";
import {server} from "./backend/mocks/server"

global.setImmediate = jest.useRealTimers as unknown as typeof setImmediate;

beforeAll(() => server.listen())

// Reset any request handlers that we may add during the tests,
// so they don"t affect other tests.
afterEach(() => server.resetHandlers())

// Clean up after the tests are finished.
afterAll(() => server.close())
