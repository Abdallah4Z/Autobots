import React from "react";

interface SocialIconProps {
  iconSrc: string;
  link: string;
  altText: string;
}

const SocialIcon: React.FC<SocialIconProps> = ({ iconSrc, link, altText }) => {
  return (
    <a
      href={link}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={`Visit my ${altText} profile`}
    >
      <img src={iconSrc} alt={`${altText} Icon`} />
    </a>
  );
};

export default SocialIcon;
