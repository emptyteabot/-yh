import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import SmartApply from './pages/SmartApply';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SmartApply />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
