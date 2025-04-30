import React from 'react';

interface AuthInputProps {
  label: string;
  type: string;
  id: string;
  value: string;
  placeholder: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  required?: boolean;
}

const AuthInput: React.FC<AuthInputProps> = ({
  label,
  type,
  id,
  value,
  placeholder,
  onChange,
  required = true,
}) => (
  <div className="form-group">
    <label htmlFor={id}>{label}</label>
    <input
      type={type}
      id={id}
      value={value}
      placeholder={placeholder}
      onChange={onChange}
      required={required}
    />
  </div>
);

export default AuthInput;
