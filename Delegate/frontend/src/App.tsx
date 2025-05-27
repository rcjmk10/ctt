import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { SnackbarProvider } from 'notistack';
import { store } from './store';
import AppWithTheme from './AppWithTheme';

function App() {
  return (
    <Provider store={store}>
      <SnackbarProvider maxSnack={3}>
        <BrowserRouter>
          <AppWithTheme />
        </BrowserRouter>
      </SnackbarProvider>
    </Provider>
  );
}

export default App;
