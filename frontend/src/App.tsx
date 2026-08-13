import { useState, useEffect } from "react";
import { AuthScreen } from "@/components/AuthScreen";
import { ChatInterface } from "@/components/ChatInterface";
import { isLoggedIn } from "@/lib/api";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    setLoggedIn(isLoggedIn());
  }, []);

  if (!loggedIn) {
    return <AuthScreen onLoginSuccess={() => setLoggedIn(true)} />;
  }

  return <ChatInterface />;
}

export default App;