import React from 'react';
import { Link } from 'react-router-dom';
import { Sprout } from 'lucide-react';

const Navbar = () => {
    return (
        <nav className="bg-white shadow-md">
            <div className="container mx-auto px-4 py-3 flex justify-between items-center">
                <Link to="/" className="flex items-center space-x-2">
                    <Sprout className="h-8 w-8 text-primary" />
                    <span className="text-xl font-bold text-gray-800">MITTI MITRA</span>
                </Link>
                <div className="space-x-4">
                    <Link to="/" className="text-gray-600 hover:text-primary transition">Home</Link>
                    <Link to="/dashboard" className="text-gray-600 hover:text-primary transition">Dashboard</Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
