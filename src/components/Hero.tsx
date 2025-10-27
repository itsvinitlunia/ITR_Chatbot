import React from 'react';
import { CheckCircle, Clock, Shield, Users } from 'lucide-react';
import { Button } from './ui/button';

const Hero: React.FC = () => {
  return (
    <section id="hero" className="bg-gradient-to-br from-blue-50 via-white to-green-50 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Welcome to
                <span className="text-blue-600 block">Professional ITR Filing</span>
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                We make income tax return filing easy and stress-free. Complete guide to Income Tax Return filing in India. Understand the process, 
                different ITR forms, eligibility criteria, and important deadlines.
              </p>
            </div>

            {/* Features */}
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-5 w-5 text-green-500" />
                <span className="text-gray-700">Complete Guide</span>
              </div>
              <div className="flex items-center space-x-3">
                <Clock className="h-5 w-5 text-green-500" />
                <span className="text-gray-700">Updated Information</span>
              </div>
              <div className="flex items-center space-x-3">
                <Shield className="h-5 w-5 text-green-500" />
                <span className="text-gray-700">Easy to Understand</span>
              </div>
              <div className="flex items-center space-x-3">
                <Users className="h-5 w-5 text-green-500" />
                <span className="text-gray-700">For All Taxpayers</span>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white text-lg px-8">
                Explore ITR Guide
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 border-blue-600 text-blue-600 hover:bg-blue-50">
                Learn Tax Basics
              </Button>
            </div>

            {/* Stats */}
            <div className="flex items-center space-x-8 pt-8 border-t border-gray-200">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">7</div>
                <div className="text-sm text-gray-600">ITR Forms</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">31 July</div>
                <div className="text-sm text-gray-600">Filing Deadline</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">Free</div>
                <div className="text-sm text-gray-600">Educational Content</div>
              </div>
            </div>
          </div>

          {/* Right Content - Image */}
          <div className="relative">
            <div className="bg-white rounded-2xl shadow-2xl p-8 transform rotate-2">
              <div className="w-full h-96 bg-gradient-to-br from-blue-100 to-green-100 rounded-lg flex items-center justify-center">
                <div className="text-center text-gray-600">
                  <div className="text-2xl font-bold mb-2">Professional Tax Consultation</div>
                  <div className="text-sm">Expert ITR Filing Assistance</div>
                </div>
              </div>
            </div>
            <div className="absolute -bottom-6 -left-6 bg-blue-600 text-white p-6 rounded-xl shadow-lg">
              <div className="text-2xl font-bold">Learn & Understand</div>
              <div className="text-sm opacity-90">ITR Filing Made Simple</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;