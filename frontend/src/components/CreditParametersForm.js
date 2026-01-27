import React, { useState } from 'react';
import axios from 'axios';
import './CreditParametersForm.css';

const CreditParametersForm = () => {
  const [formData, setFormData] = useState({
    // User and basic info
    user: '',
    name: '',
    
    // Categorical Fields
    occupation: '',
    delay_from_due_date: '',
    credit_mix: '',
    payment_of_minimum_amount: '',
    payment_behaviour: '',
    changed_credit_limit: '',
    
    // Numerical Fields
    age: '',
    annual_income: '',
    monthly_in_hand_salary: '',
    number_of_bank_accounts: '',
    number_of_credit_cards: '',
    interest_rate: '',
    number_of_loans: '',
    number_of_delayed_payment: '',
    num_credit_inquiries: '',
    outstanding_debt: '',
    credit_utilization_ratio: '',
    total_emi_per_month: '',
    amount_invested_monthly: '',
    monthly_balance: ''
  });

  const [submitStatus, setSubmitStatus] = useState({ message: '', type: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const paymentBehaviourOptions = [
    { value: 'low_spend_small_value_payments', label: 'Low Spend, Small Value Payments' },
    { value: 'low_spend_medium_value_payments', label: 'Low Spend, Medium Value Payments' },
    { value: 'low_spend_large_value_payments', label: 'Low Spend, Large Value Payments' },
    { value: 'high_spend_small_value_payments', label: 'High Spend, Small Value Payments' },
    { value: 'high_spend_medium_value_payments', label: 'High Spend, Medium Value Payments' },
    { value: 'high_spend_large_value_payments', label: 'High Spend, Large Value Payments' }
  ];

  const yesNoOptions = [
    { value: 'Yes', label: 'Yes' },
    { value: 'No', label: 'No' }
  ];

  const creditMixOptions = [
    { value: 'Good', label: 'Good' },
    { value: 'Standard', label: 'Standard' },
    { value: 'Bad', label: 'Bad' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus({ message: '', type: '' });

    try {
      const response = await axios.post('/calculate/credit-parameters/', formData);
      setSubmitStatus({
        message: `Success! Credit Score: ${response.data.credit_score || 'Pending'}`,
        type: 'success'
      });
      
      // Reset form after successful submission
      setFormData({
        user: '', name: '', occupation: '', delay_from_due_date: '',
        credit_mix: '', payment_of_minimum_amount: '', payment_behaviour: '',
        changed_credit_limit: '', age: '', annual_income: '',
        monthly_in_hand_salary: '', number_of_bank_accounts: '', number_of_credit_cards: '',
        interest_rate: '', number_of_loans: '', number_of_delayed_payment: '',
        num_credit_inquiries: '', outstanding_debt: '', credit_utilization_ratio: '',
        total_emi_per_month: '', amount_invested_monthly: '', monthly_balance: ''
      });
    } catch (error) {
      console.error('Error submitting form:', error);
      let errorMessage = 'Failed to submit';
      
      if (error.response?.data) {
        // If there are field-specific errors, display them
        const errors = error.response.data;
        if (typeof errors === 'object') {
          errorMessage = Object.entries(errors)
            .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
            .join(' | ');
        } else {
          errorMessage = errors.toString();
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setSubmitStatus({
        message: `Error: ${errorMessage}`,
        type: 'error'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <h1>Credit Parameters Form</h1>
      {submitStatus.message && (
        <div className={`alert alert-${submitStatus.type}`}>
          {submitStatus.message}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h2>Personal Information</h2>
          
          <div className="form-group">
            <label htmlFor="user">User Email:</label>
            <input
              type="email"
              id="user"
              name="user"
              placeholder="Enter user email"
              value={formData.user}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="age">Age:</label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="occupation">Occupation:</label>
            <input
              type="text"
              id="occupation"
              name="occupation"
              value={formData.occupation}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-section">
          <h2>Financial Information</h2>

          <div className="form-group">
            <label htmlFor="annual_income">Annual Income (£):</label>
            <input
              type="number"
              step="0.01"
              id="annual_income"
              name="annual_income"
              value={formData.annual_income}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="monthly_in_hand_salary">Monthly In-Hand Salary (£):</label>
            <input
              type="number"
              step="0.01"
              id="monthly_in_hand_salary"
              name="monthly_in_hand_salary"
              value={formData.monthly_in_hand_salary}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="monthly_balance">Monthly Balance (£):</label>
            <input
              type="number"
              step="0.01"
              id="monthly_balance"
              name="monthly_balance"
              value={formData.monthly_balance}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="amount_invested_monthly">Amount Invested Monthly (£):</label>
            <input
              type="number"
              step="0.01"
              id="amount_invested_monthly"
              name="amount_invested_monthly"
              value={formData.amount_invested_monthly}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-section">
          <h2>Credit Information</h2>

          <div className="form-group">
            <label htmlFor="number_of_bank_accounts">Number of Bank Accounts:</label>
            <input
              type="number"
              id="number_of_bank_accounts"
              name="number_of_bank_accounts"
              value={formData.number_of_bank_accounts}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="number_of_credit_cards">Number of Credit Cards:</label>
            <input
              type="number"
              id="number_of_credit_cards"
              name="number_of_credit_cards"
              value={formData.number_of_credit_cards}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="number_of_loans">Number of Loans:</label>
            <input
              type="number"
              id="number_of_loans"
              name="number_of_loans"
              value={formData.number_of_loans}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="interest_rate">Interest Rate (%):</label>
            <input
              type="number"
              step="0.01"
              id="interest_rate"
              name="interest_rate"
              value={formData.interest_rate}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="credit_mix">Credit Mix:</label>
            <select
              id="credit_mix"
              name="credit_mix"
              value={formData.credit_mix}
              onChange={handleChange}
              required
            >
              <option value="">Select credit mix</option>
              {creditMixOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="outstanding_debt">Outstanding Debt (£):</label>
            <input
              type="number"
              step="0.01"
              id="outstanding_debt"
              name="outstanding_debt"
              value={formData.outstanding_debt}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="credit_utilization_ratio">Credit Utilization Ratio (%):</label>
            <input
              type="number"
              step="0.01"
              id="credit_utilization_ratio"
              name="credit_utilization_ratio"
              value={formData.credit_utilization_ratio}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="total_emi_per_month">Total EMI per Month (£):</label>
            <input
              type="number"
              step="0.01"
              id="total_emi_per_month"
              name="total_emi_per_month"
              value={formData.total_emi_per_month}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-section">
          <h2>Payment Information</h2>

          <div className="form-group">
            <label htmlFor="payment_behaviour">Payment Behaviour:</label>
            <select
              id="payment_behaviour"
              name="payment_behaviour"
              value={formData.payment_behaviour}
              onChange={handleChange}
              required
            >
              <option value="">Select payment behaviour</option>
              {paymentBehaviourOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="payment_of_minimum_amount">Payment of Minimum Amount:</label>
            <select
              id="payment_of_minimum_amount"
              name="payment_of_minimum_amount"
              value={formData.payment_of_minimum_amount}
              onChange={handleChange}
              required
            >
              <option value="">Select option</option>
              {yesNoOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="number_of_delayed_payment">Number of Delayed Payments:</label>
            <input
              type="number"
              id="number_of_delayed_payment"
              name="number_of_delayed_payment"
              value={formData.number_of_delayed_payment}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="delay_from_due_date">Delay from Due Date (days):</label>
            <input
              type="text"
              id="delay_from_due_date"
              name="delay_from_due_date"
              value={formData.delay_from_due_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="changed_credit_limit">Changed Credit Limit:</label>
            <select
              id="changed_credit_limit"
              name="changed_credit_limit"
              value={formData.changed_credit_limit}
              onChange={handleChange}
              required
            >
              <option value="">Select option</option>
              {yesNoOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="num_credit_inquiries">Number of Credit Inquiries:</label>
            <input
              type="number"
              id="num_credit_inquiries"
              name="num_credit_inquiries"
              value={formData.num_credit_inquiries}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <button type="submit" disabled={isSubmitting} className="submit-button">
          {isSubmitting ? 'Submitting...' : 'Calculate Credit Score'}
        </button>
      </form>
    </div>
  );
};

export default CreditParametersForm;
