import React from 'react';
import {render, screen} from '@testing-library/react';
import {Lobby} from "./components/Lobby";

test('renders lobby screen', () => {
  render(<Lobby onNewGame={() => null}/>);
  const linkElement = screen.getByText(/Welcome to tic tac toe!/i);
  expect(linkElement).toBeInTheDocument();
});
