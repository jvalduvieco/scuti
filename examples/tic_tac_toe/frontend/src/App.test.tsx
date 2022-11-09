import React from 'react';
import {screen} from '@testing-library/react';
import {Lobby} from "./components/Lobby";
import {renderWithProviders} from "./utils/test";

test('renders lobby screen', async () => {
  renderWithProviders(<Lobby/>);
  const linkElement = await screen.findByText(/Welcome to tic tac toe!/i);
  expect(linkElement).toBeInTheDocument();
});
