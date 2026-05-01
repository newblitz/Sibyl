import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import { Zap, Lock, Calendar, Video, MessageCircle, TrendingUp } from 'lucide-react';
import '../styles/Features.css';

function Features() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start'],
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);

  const features = [
    {
      icon: Zap,
      title: 'Instant Matching',
      description: 'Get matched with the right therapist in under 2 minutes using our intelligent matching system.',
    },
    {
      icon: Lock,
      title: 'Private & Secure',
      description: 'End-to-end encryption ensures your conversations remain completely confidential.',
    },
    {
      icon: Calendar,
      title: 'Flexible Scheduling',
      description: 'Book sessions that fit your schedule, with options for same-day appointments.',
    },
    {
      icon: Video,
      title: 'Virtual Sessions',
      description: 'High-quality video sessions from the comfort of your home or anywhere you feel safe.',
    },
    {
      icon: MessageCircle,
      title: 'Chat Anytime',
      description: 'Message your therapist between sessions and get support when you need it most.',
    },
    {
      icon: TrendingUp,
      title: 'Track Progress',
      description: 'Visualize your mental health journey with insightful analytics and milestone tracking.',
    },
  ];

  return (
    <section ref={ref} className="features" id="features">
      <div className="features-container">
        <motion.div
          className="features-header"
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.6 }}
        >
          <motion.div
            className="header-badge"
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
          >
            Features
          </motion.div>
          <h2 className="section-title">
            Everything you need to
            <br />
            <span className="gradient-text">transform your mindset</span>
          </h2>
          <p className="section-subtitle">
            Professional tools and support designed for your wellness journey
          </p>
        </motion.div>

        <motion.div className="features-grid">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="feature-card"
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -8 }}
            >
              <div className="feature-icon-container">
                <feature.icon size={24} strokeWidth={2} />
              </div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          className="features-spotlight"
          style={{ y }}
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="spotlight-content">
            <div className="spotlight-visual">
              <motion.div
                className="spotlight-glow"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 0.8, 0.5],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
              />
              <div className="spotlight-card">
                <div className="card-header">
                  <div className="avatar">👤</div>
                  <div className="card-info">
                    <div className="therapist-name">Dr. Sarah Johnson</div>
                    <div className="therapist-title">Clinical Psychologist</div>
                  </div>
                  <div className="status-badge">Available</div>
                </div>
                <div className="card-stats">
                  <div className="stat">
                    <div className="stat-value">4.9</div>
                    <div className="stat-label">Rating</div>
                  </div>
                  <div className="stat">
                    <div className="stat-value">1,200+</div>
                    <div className="stat-label">Sessions</div>
                  </div>
                  <div className="stat">
                    <div className="stat-value">8 yrs</div>
                    <div className="stat-label">Experience</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="spotlight-text">
              <h3>Meet your perfect match</h3>
              <p>
                Our intelligent matching algorithm connects you with therapists who
                specialize in your specific needs and concerns.
              </p>
              <motion.a
                href="#therapists"
                className="btn-link"
                whileHover={{ x: 5 }}
              >
                Browse therapists →
              </motion.a>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

export default Features;
