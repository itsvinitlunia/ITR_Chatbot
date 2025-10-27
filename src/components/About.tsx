import React from "react";
import { Badge } from "./ui/badge";
import { Card, CardContent } from "./ui/card";
import { FileText, Calendar, Users, Calculator, CheckCircle, Target, Info } from "lucide-react";

function About() {
  const keyFacts = [
    { icon: FileText, number: "7", label: "Different ITR Forms" },
    { icon: Calendar, number: "31 July", label: "Filing Deadline" },
    { icon: Users, number: "6.8 Cr", label: "Returns Filed (2023)" },
    { icon: Calculator, number: "₹2.5L", label: "Basic Exemption Limit" }
  ];

  const importantTopics = [
    "Understanding Income Tax Slabs",
    "Deductions under Section 80C",
    "TDS and Advance Tax",
    "E-filing Process",
    "Penalty for Late Filing",
    "Tax Refund Process"
  ];

  const taxSlabsNewRegime = [
    { income: "₹0 – ₹3,00,000", rate: "Nil" },
    { income: "₹3,00,001 – ₹7,00,000", rate: "5%" },
    { income: "₹7,00,001 – ₹10,00,000", rate: "10%" },
    { income: "₹10,00,001 – ₹12,00,000", rate: "15%" },
    { income: "₹12,00,001 – ₹15,00,000", rate: "20%" },
    { income: "Above ₹15,00,000", rate: "30%" }
  ];

  return (
    <section id="about" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center space-y-4 mb-16">
          <Badge variant="secondary" className="px-4 py-2">About Income Tax Returns</Badge>
          <h2 className="text-4xl font-bold text-gray-900">
            Everything You Need to Know About ITR
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Income Tax Return (ITR) is a document that taxpayers file with the Income Tax Department to report their income, expenses, and tax liability for a financial year.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-16">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-6">
              <h3 className="text-3xl font-bold text-gray-900">
                What is Income Tax Return?
              </h3>
              <p className="text-lg text-gray-600">
                An Income Tax Return (ITR) is a form used to file information about your income and tax with the Income Tax Department. It contains details of your income from various sources, deductions claimed, and taxes paid.
              </p>
              <p className="text-lg text-gray-600">
                Filing ITR is mandatory for individuals whose income exceeds the basic exemption limit or those who want to claim a tax refund.
              </p>
            </div>
            {/* Important Topics */}
            <div className="space-y-4">
              <h4 className="text-xl font-semibold text-gray-900">Key Topics to Understand</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {importantTopics.map((topic, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{topic}</span>
                  </div>
                ))}
              </div>
            </div>
            {/* Why File ITR */}
            <Card className="bg-gradient-to-r from-blue-50 to-green-50 border-none">
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="bg-primary text-white p-3 rounded-lg">
                    <Target className="w-6 h-6" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Why File ITR?</h4>
                    <p className="text-gray-600">
                      Filing ITR helps in claiming refunds, serves as income proof for loans, and maintains financial transparency.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
          {/* Right Content - Stats */}
          <div className="space-y-8">
            {/* Key Facts */}
            <div className="grid grid-cols-2 gap-6">
              {keyFacts.map((fact, index) => {
                const IconComponent = fact.icon;
                return (
                  <Card key={index} className="text-center border-none shadow-lg">
                    <CardContent className="p-6 space-y-4">
                      <div className="bg-primary/10 text-primary p-3 rounded-full w-fit mx-auto">
                        <IconComponent className="w-6 h-6" />
                      </div>
                      <div className="text-3xl font-bold text-primary">{fact.number}</div>
                      <div className="text-sm text-gray-600">{fact.label}</div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        </div>

        {/* Tax Slabs Information - FY 2024-25 New Regime (Default) */}
        <Card className="bg-gray-50">
          <CardContent className="p-8">
            <div className="text-center mb-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Income Tax Slabs (FY 2024-25) – New Regime</h3>
              <p className="text-gray-600">Default regime for individuals. Rebate under Section 87A may apply.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {taxSlabsNewRegime.map((slab, index) => (
                <Card key={index} className="text-center">
                  <CardContent className="p-6 space-y-4">
                    <div className="text-2xl font-bold text-primary">{slab.rate}</div>
                    <div className="font-medium text-gray-900">{slab.income}</div>
                  </CardContent>
                </Card>
              ))}
            </div>
            <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-start space-x-3">
                <Info className="w-5 h-5 text-blue-600 mt-0.5" />
                <div className="text-sm text-blue-800">
                  <strong>Note:</strong> Old Regime slabs (optional): 0–₹2,50,000 Nil; ₹2,50,001–₹5,00,000 5%; ₹5,00,001–₹10,00,000 20%; Above ₹10,00,000 30%.
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}

export default About;