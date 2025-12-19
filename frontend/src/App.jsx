import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Predict from './pages/Predict';
import ManualInput from './pages/ManualInput';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-100 font-sans">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-lg z-10 hidden md:flex flex-col">
          <div className="p-6 border-b border-green-100 bg-green-50">
            <h1 className="text-2xl font-extrabold text-green-800 tracking-tight flex items-center">
              <span className="mr-2">🌾</span> Mitti Mitra
            </h1>
            <p className="text-xs text-green-600 mt-1 uppercase tracking-wider font-semibold">Farmer's Assistant</p>
          </div>

          <nav className="flex-1 px-4 py-6 space-y-2">
            <NavLink
              to="/"
              className={({ isActive }) => `flex items-center px-4 py-3 rounded-lg transition-all duration-200 ${isActive ? 'bg-green-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100 hover:text-green-700'}`}
            >
              <span className="mr-3">📊</span> Dashboard
            </NavLink>
            <NavLink
              to="/predict"
              className={({ isActive }) => `flex items-center px-4 py-3 rounded-lg transition-all duration-200 ${isActive ? 'bg-green-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100 hover:text-green-700'}`}
            >
              <span className="mr-3">🧠</span> AI Predictor
            </NavLink>
            <NavLink
              to="/manual"
              className={({ isActive }) => `flex items-center px-4 py-3 rounded-lg transition-all duration-200 ${isActive ? 'bg-green-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100 hover:text-green-700'}`}
            >
              <span className="mr-3">📝</span> Manual Input
            </NavLink>
          </nav>

          <div className="p-4 border-t border-gray-100">
            <div className="text-xs text-gray-400 text-center">
              &copy; 2025 Mitti Mitra Project
            </div>
          </div>
        </aside>

        {/* Mobile Nav (Simple Top Bar) */}
        <div className="md:hidden fixed top-0 w-full bg-green-600 text-white z-20 flex justify-between p-4 shadow-md">
          <span className="font-bold">Mitti Mitra</span>
          {/* Mobile menu toggle would go here */}
        </div>

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto p-4 md:p-8 pt-20 md:pt-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/manual" element={<ManualInput />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
