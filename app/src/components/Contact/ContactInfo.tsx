import React from "react";
import contactData from "../../data/contactInfo.json";
import SocialIcon from "./SocialIcon"; // Import the SocialIcon component

import facebookIcon from '../../assets/facebook.svg';
import gitHubIcon from '../../assets/github.svg';
import linkedInIcon from '../../assets/linkedin.svg';
import instagramIcon from '../../assets/instagram.svg';
import discordIcon from '../../assets/discord.svg';


const ContactInfo: React.FC = () => {
  const { name, bio, links } = contactData;

  const socialLinks = [
    {
      icon: facebookIcon,
      link: "#",
      altText: "Facebook"
    },
    {
      icon: gitHubIcon,
      link: "#",
      altText: "GitHub"
    },
    {
      icon: linkedInIcon,
      link: "#",
      altText: "LinkedIn"
    },
    {
      icon: instagramIcon,
      link: "#",
      altText: "Instagram"
    },
    {
      icon: discordIcon,
      link: "#",
      altText: "Discord"
    }
  ];

  return (
    <div className="contact-info">
      <h1>{name}</h1>
      {bio && <p className="bio">{bio}</p>} {/* Display bio if available */}

      <div className="contact_boxes">
        {links.map((link: { label: string, url: string }) => (
          <div key={link.label} className="item">
            <a href={link.url} target="_blank" rel="noopener noreferrer">
              {link.label}
            </a>
          </div>
        ))}
      </div>

      <div className="social-icons">
        {socialLinks.map((social) => (
          <SocialIcon
            key={social.altText}
            iconSrc={social.icon}
            link={social.link}
            altText={social.altText}
          />
        ))}
      </div>
    </div>
  );
};

export default ContactInfo;
