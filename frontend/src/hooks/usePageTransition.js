import { useState, useEffect } from "react";

export const usePageTransition = () => {
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [currentView, setCurrentView] = useState(null);

  const transitionTo = (newView, callback) => {
    setIsTransitioning(true);

    // Wait for exit animation
    setTimeout(() => {
      setCurrentView(newView);

      // Wait for enter animation
      setTimeout(() => {
        setIsTransitioning(false);
        if (callback) callback();
      }, 300);
    }, 300);
  };

  return {
    isTransitioning,
    currentView,
    transitionTo,
  };
};
