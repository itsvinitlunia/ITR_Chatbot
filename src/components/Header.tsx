import React from 'react'
import { Button } from "./ui/button"
import { Menu, X } from "lucide-react"
import { useState } from "react"

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header className="bg-white shadow-sm border-b sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-2xl font-bold text-blue-600">ITR Learn Hub</h1>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <a href="#home" className="text-gray-900 hover:text-blue-600 px-3 py-2 transition-colors">
                Home
              </a>
              <a href="#services" className="text-gray-600 hover:text-blue-600 px-3 py-2 transition-colors">
                ITR Guide
              </a>
              <a href="#about" className="text-gray-600 hover:text-blue-600 px-3 py-2 transition-colors">
                About
              </a>
              <a href="#contact" className="text-gray-600 hover:text-blue-600 px-3 py-2 transition-colors">
                Contact
              </a>
            </div>
          </nav>

          {/* CTA Button */}
          <div className="hidden md:block">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              Learn More
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600 hover:text-blue-600 focus:outline-none focus:text-blue-600"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <a href="#home" className="block text-gray-900 hover:text-blue-600 px-3 py-2 rounded-md">Home</a>
              <a href="#services" className="block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md">ITR Guide</a>
              <a href="#about" className="block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md">About</a>
              <a href="#contact" className="block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md">Contact</a>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header