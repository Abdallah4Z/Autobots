import React from "react";
import "../style/contact_style.css";
import ContactInfo from "../components/Contact/ContactInfo";
import ContactForm from "../components/Contact/ContactForm";

const ContactPage: React.FC = () => {
  return (
    <div className="container">
      <ContactInfo />
      <ContactForm />
    </div>
  );
};

export default ContactPage;
