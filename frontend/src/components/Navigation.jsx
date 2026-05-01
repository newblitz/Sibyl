import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import '../styles/Navigation.css';

function Navigation() {
  const [scrolled, setScrolled] = useState(false);
  const [isAuthenticated] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'Features', href: '#features' },
    { name: 'Therapists', href: '#therapists' },
    { name: 'Pricing', href: '#pricing' },
    { name: 'Careers', href: '/internship' },
  ];

  return (
    <motion.header
      className={`navigation ${scrolled ? 'scrolled' : ''}`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      <div className="nav-container">
        <motion.a
          href="/"
          className="logo"
          whileHover={{ opacity: 0.8 }}
        >
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect width="28" height="28" rx="6" fill="currentColor" />
            <path
              d="M14 8L18 12L14 16M10 12H18"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="logo-text">MindEase</span>
        </motion.a>

        <nav className="nav-links">
          {navLinks.map((link) => (
            <motion.a
              key={link.name}
              href={link.href}
              className="nav-link"
              whileHover={{ y: -1 }}
            >
              {link.name}
            </motion.a>
          ))}
        </nav>

        <div className="nav-actions">
          {isAuthenticated ? (
            <>
              <span className="user-indicator">👤</span>
              <motion.a
                href="/logout"
                className="btn-nav"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Logout
              </motion.a>
            </>
          ) : (
            <>
              <motion.a
                href="/create/login/"
                className="btn-nav btn-ghost"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Sign in
              </motion.a>
              <motion.a
                href="/create/"
                className="btn-nav btn-primary"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Get Started
              </motion.a>
            </>
          )}
        </div>

        <motion.button
          className="mobile-menu-btn"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          whileTap={{ scale: 0.95 }}
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </motion.button>
      </div>

      {mobileMenuOpen && (
        <motion.div
          className="mobile-menu"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
        >
          {navLinks.map((link) => (
            <a key={link.name} href={link.href} className="mobile-link">
              {link.name}
            </a>
          ))}
          <div className="mobile-actions">
            <a href="/create/login/" className="mobile-action">
              Sign in
            </a>
            <a href="/create/" className="mobile-action primary">
              Get Started
            </a>
          </div>
        </motion.div>
      )}
    </motion.header>
  );
}

export default Navigation;
