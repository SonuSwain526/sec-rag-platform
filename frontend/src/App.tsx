import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthScreen } from "@/components/AuthScreen";
import { ChatInterface } from "@/components/ChatInterface";
import { DocsPage } from "@/components/DocsPage";
import { Navbar } from "@/components/Navbar";
import { isLoggedIn } from "@/lib/api";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    setLoggedIn(isLoggedIn());
  }, []);

  if (!loggedIn) {
    return <AuthScreen onLoginSuccess={() => setLoggedIn(true)} />;
  }

  return (
    <BrowserRouter>
      <Navbar onLogout={() => setLoggedIn(false)} />
      <Routes>
        <Route path="/" element={<ChatInterface />} />
        <Route path="/docs" element={<DocsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;