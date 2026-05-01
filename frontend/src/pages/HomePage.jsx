import { motion } from 'framer-motion';
import { Brain, Calendar, Shield, Clock, CheckCircle, MessageCircle } from 'lucide-react';
import Navigation from '../components/Navigation';
import Hero from '../components/Hero';
import Features from '../components/Features';
import Benefits from '../components/Benefits';
import Footer from '../components/Footer';
import '../styles/HomePage.css';

function HomePage() {
  return (
    <div className="homepage">
      <Navigation />
      <Hero />
      <Features />
      <Benefits />
      <Footer />
    </div>
  );
}

export default HomePage;
