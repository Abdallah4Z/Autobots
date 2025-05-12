import React from "react";
import { Link } from "react-router-dom"; // If you're using React Router for navigation

const ContactForm: React.FC = () => {
  return (
    <div className="form-section">
      <h2>Found a bug or issue?</h2>
      <p>Let me know what's wrong — your feedback helps improve the experience!</p>
      
      <form  method="POST">
        <input
          type="text"
          name="name"
          placeholder="Your name"
          required
        />
        <input
          type="email"
          name="email"
          placeholder="your@email.com"
          required
        />
        <textarea
          name="message"
          placeholder="Describe the bug or issue in detail..."
          required
        ></textarea>
        
        {/* Container for the buttons */}
        <div className="button-container">
          <button className="submit-button" type="submit">Report Issue</button>
          <Link to="/" className="home-link">
            <button type="button" className="home-button">Home</button>
          </Link>
        </div>
      </form>
    </div>
  );
};

export default ContactForm;
