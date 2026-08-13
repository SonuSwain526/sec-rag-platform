import { useState, useEffect } from "react";
import { AuthScreen } from "@/components/AuthScreen";
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
    <div className="flex min-h-screen items-center justify-center">
      <p>Logged in! Chat interface goes here next.</p>
    </div>
  );
}

export default App;