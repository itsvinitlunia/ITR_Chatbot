import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Button } from "./ui/button"
import { Badge } from "./ui/badge"
import { 
  FileText, 
  Users, 
  Building, 
  Briefcase,
  ArrowRight,
  Clock,
  CheckCircle
} from "lucide-react"

export function Services() {
  const itrForms = [
    {
      icon: FileText,
      title: "ITR-1 (Sahaj)",
      description: "For individuals having income from salary, one house property, other sources",
      eligibility: "Income up to ₹50 lakhs",
      features: ["Salary Income", "One House Property", "Interest Income"],
      category: "Individual"
    },
    {
      icon: Users,
      title: "ITR-2",
      description: "For individuals and HUFs not having income from business or profession",
      eligibility: "Multiple sources of income",
      features: ["Multiple Properties", "Capital Gains", "Foreign Assets"],
      category: "Individual/HUF"
    },
    {
      icon: Building,
      title: "ITR-3",
      description: "For individuals and HUFs having income from business or profession",
      eligibility: "Business/Professional income",
      features: ["Business Income", "Professional Income", "Partnership"],
      category: "Business"
    },
    {
      icon: Briefcase,
      title: "ITR-4 (Sugam)",
      description: "For presumptive income from business and profession",
      eligibility: "Presumptive taxation scheme",
      features: ["Section 44AD", "Section 44ADA", "Up to ₹2 Crores"],
      category: "Presumptive"
    }
  ]

  const filingSteps = [
    {
      step: "1",
      title: "Gather Documents",
      description: "Collect Form 16, bank statements, investment proofs"
    },
    {
      step: "2", 
      title: "Choose ITR Form",
      description: "Select appropriate ITR form based on income sources"
    },
    {
      step: "3",
      title: "Fill Details",
      description: "Enter personal information, income, and deductions"
    },
    {
      step: "4",
      title: "Verify & Submit",
      description: "Review details and e-verify using Aadhaar OTP"
    }
  ]

  return (
    <section id="services" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center space-y-4 mb-16">
          <Badge variant="secondary" className="px-4 py-2">ITR Information</Badge>
          <h2 className="text-4xl font-bold text-gray-900">
            Understanding Different ITR Forms
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Learn about the different Income Tax Return forms and their eligibility criteria.
          </p>
        </div>

        {/* ITR Forms Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {itrForms.map((form, index) => {
            const IconComponent = form.icon
            return (
              <Card key={index} className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                <CardHeader className="text-center space-y-4">
                  <div className="mx-auto w-16 h-16 rounded-2xl bg-blue-100 text-primary flex items-center justify-center">
                    <IconComponent className="w-8 h-8" />
                  </div>
                  
                  <div>
                    <CardTitle className="text-xl mb-2">{form.title}</CardTitle>
                    <Badge variant="outline" className="mb-3">{form.category}</Badge>
                    <CardDescription className="text-gray-600">
                      {form.description}
                    </CardDescription>
                  </div>

                  <div className="p-3 bg-green-50 rounded-lg">
                    <p className="text-sm font-medium text-green-800">{form.eligibility}</p>
                  </div>
                </CardHeader>

                <CardContent className="space-y-6">
                  <ul className="space-y-3">
                    {form.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center text-sm text-gray-600">
                        <CheckCircle className="w-4 h-4 text-green-500 mr-3 flex-shrink-0" />
                        {feature}
                      </li>
                    ))}
                  </ul>

                  <Button variant="outline" className="w-full">
                    Learn More
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Filing Process */}
        <div className="bg-white rounded-2xl p-8 shadow-lg">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">ITR Filing Process</h3>
            <p className="text-lg text-gray-600">Step-by-step guide to filing your Income Tax Return</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {filingSteps.map((step, index) => (
              <div key={index} className="relative">
                <div className="text-center space-y-4">
                  <div className="mx-auto w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-xl font-bold">
                    {step.step}
                  </div>
                  <h4 className="font-semibold text-gray-900">{step.title}</h4>
                  <p className="text-gray-600 text-sm">{step.description}</p>
                </div>
                {index < filingSteps.length - 1 && (
                  <div className="hidden lg:block absolute top-8 left-full w-full">
                    <div className="w-8 h-0.5 bg-gray-300 transform -translate-x-4"></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Important Information */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="bg-blue-50 border-blue-200">
            <CardContent className="p-6 text-center space-y-4">
              <Clock className="w-12 h-12 text-blue-600 mx-auto" />
              <h4 className="font-semibold text-blue-900">Filing Deadline</h4>
              <p className="text-blue-800">ITR filing deadline is 31st July. Late filing attracts penalty.</p>
            </CardContent>
          </Card>

          <Card className="bg-green-50 border-green-200">
            <CardContent className="p-6 text-center space-y-4">
              <FileText className="w-12 h-12 text-green-600 mx-auto" />
              <h4 className="font-semibold text-green-900">Documentation</h4>
              <p className="text-green-800">Keep Form 16, bank statements, and investment proofs ready.</p>
            </CardContent>
          </Card>

          <Card className="bg-purple-50 border-purple-200">
            <CardContent className="p-6 text-center space-y-4">
              <Users className="w-12 h-12 text-purple-600 mx-auto" />
              <h4 className="font-semibold text-purple-900">Eligibility</h4>
              <p className="text-purple-800">Filing is mandatory if income exceeds basic exemption limit.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}

export default Services;