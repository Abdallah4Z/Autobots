import React from 'react';
import { Container, Typography, Accordion, AccordionSummary, AccordionDetails, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Layout from '../components/Layout';

const FAQsPage: React.FC = () => {
  // FAQ data
  const faqs = [
    {
      question: "How do I find the optimal route between two locations?",
      answer: "Enter your starting point and destination in the search fields on the main dashboard. The system will automatically calculate the most efficient route based on current traffic conditions, distance, and available transportation options."
    },
    {
      question: "Can I compare different transportation methods?",
      answer: "Yes! After entering your route, you can view various transportation options including bus, metro, walking, and mixed modes. Each option displays the estimated time, distance, and any transfers required."
    },
    {
      question: "How accurate is the travel time estimation?",
      answer: "Our travel time estimates are based on real-time data and historical patterns. They account for average speeds, typical delays, and scheduled transportation times. However, unexpected events may affect actual travel times."
    },
    {
      question: "Is there an emergency routing option?",
      answer: "Yes, our emergency routing feature provides the fastest path to hospitals, police stations, or other emergency services. Access this feature from the Emergency Routing section in the main menu."
    },
    {
      question: "How do I report an issue with a suggested route?",
      answer: "You can report issues through the Contact page. Please provide specific details about the route, the problem encountered, and any alternative routes you may have taken."
    },
    {
      question: "Can I save my frequent routes?",
      answer: "Currently, this feature is under development. In the future release, you will be able to save your favorite routes for quick access."
    },
    {
      question: "Does the system account for public transportation schedules?",
      answer: "Yes, our route planning incorporates the schedules of buses and metro lines. The system considers waiting times between connections when calculating total travel time."
    }
  ];

  // Set document title
  React.useEffect(() => {
    document.title = "FAQs - Transportation Network";
  }, []);

  return (
    <Layout>
      <Container maxWidth="md" sx={{ py: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
          Frequently Asked Questions
        </Typography>
        
        <Box sx={{ mb: 6 }}>
          <Typography variant="body1" paragraph>
            Find answers to common questions about our transportation network optimization system. 
            If you don't see your question here, feel free to reach out through our Contact page.
          </Typography>
        </Box>

        {faqs.map((faq, index) => (
          <Accordion key={index} sx={{ mb: 2 }}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls={`panel${index}-content`}
              id={`panel${index}-header`}
            >
              <Typography variant="h6">{faq.question}</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography>{faq.answer}</Typography>
            </AccordionDetails>
          </Accordion>
        ))}
      </Container>
    </Layout>
  );
};

export default FAQsPage;
