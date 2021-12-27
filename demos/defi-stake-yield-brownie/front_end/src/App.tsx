import React from 'react';


import { DAppProvider, ChainId } from "@usedapp/core"
import { Header } from './components/Header'
import { Container } from '@material-ui/core'
import { Main } from './components/Main'

function App() {
  return (
    <DAppProvider config={{
      supportedChains: [ChainId.Kovan],
      notifications: {  // to check the blockchain work collectly or not
        expirationPeriod: 1000, // 1 sec
        checkInterval: 1000,
      }
    }}>
      <Header />
      <Container maxWidth='md'>
        <Main />
      </Container>
    </DAppProvider>
  );
}

export default App;
