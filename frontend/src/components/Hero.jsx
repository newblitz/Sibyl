import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowRight, Sparkles, Play } from 'lucide-react';
import { useRef } from 'react';
import '../styles/Hero.css';

function Hero() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start start', 'end start'],
  });

  const y = useTransform(scrollYProgress, [0, 1], ['0%', '50%']);
  const opacity = useTransform(scrollYProgress, [0, 1], [1, 0]);

  return (
    <section ref={ref} className="hero">
      <div className="hero-grid" />

      <motion.div className="hero-glow" style={{ opacity }} />

      <div className="hero-container">
        <motion.div
          className="hero-content"
          style={{ y, opacity }}
        >
          <motion.div
            className="hero-badge"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <span className="badge-dot" />
            <span>Professional Mental Health Support</span>
          </motion.div>

          <motion.h1
            className="hero-title"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            Design your path to
            <br />
            <span className="gradient-text">mental wellness</span>
          </motion.h1>

          <motion.p
            className="hero-description"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Connect with licensed therapists who understand your journey.
            Start building a healthier mind today.
          </motion.p>

          <motion.div
            className="hero-actions"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <motion.a
              href="/appointment"
              className="btn btn-primary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Start for Free
              <ArrowRight size={18} strokeWidth={2} />
            </motion.a>

            <motion.button
              className="btn btn-play"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="play-icon">
                <Play size={14} fill="currentColor" />
              </div>
              <span>Watch Demo</span>
            </motion.button>
          </motion.div>

          <motion.div
            className="hero-trust"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="trust-avatars">
              <div className="avatar">🧑</div>
              <div className="avatar">👨</div>
              <div className="avatar">👩</div>
              <div className="avatar">🧑‍🦱</div>
            </div>
            <div className="trust-text">
              <strong>2,000+</strong> people started their journey this month
            </div>
          </motion.div>
        </motion.div>

        <motion.div
          className="hero-visual"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="visual-card main-card">
            <motion.div
              className="card-pulse"
              animate={{
                scale: [1, 1.1, 1],
                opacity: [0.5, 0.8, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
            <div className="card-content">
              <div className="card-header">
                <div className="status-indicator">
                  <span className="status-dot" />
                  <span>Available Now</span>
                </div>
              </div>
              <div className="card-body">
                <h3>Your Wellness Journey</h3>
                <div className="progress-ring">
                  <svg viewBox="0 0 100 100">
                    <defs>
                      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#0ea5e9" />
                        <stop offset="100%" stopColor="#6366f1" />
                      </linearGradient>
                    </defs>
                    <circle cx="50" cy="50" r="45" />
                    <motion.circle
                      cx="50"
                      cy="50"
                      r="45"
                      initial={{ pathLength: 0 }}
                      animate={{ pathLength: 0.75 }}
                      transition={{ duration: 2, ease: 'easeOut' }}
                    />
                  </svg>
                  <div className="progress-value">75%</div>
                </div>
              </div>
            </div>
          </div>

          <motion.div
            className="visual-card floating-stat stat-1"
            animate={{
              y: [0, -10, 0],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          >
            <Sparkles size={20} />
            <div>
              <div className="stat-value">98%</div>
              <div className="stat-label">Satisfaction</div>
            </div>
          </motion.div>

          <motion.div
            className="visual-card floating-stat stat-2"
            animate={{
              y: [0, -15, 0],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: 'easeInOut',
              delay: 0.5,
            }}
          >
            <div className="stat-icon">⚡</div>
            <div>
              <div className="stat-value">24/7</div>
              <div className="stat-label">Support</div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}

export default Hero;
