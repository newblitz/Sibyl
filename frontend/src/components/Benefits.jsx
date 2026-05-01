import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import '../styles/Benefits.css';

function Benefits() {
  const stats = [
    { value: '10,000+', label: 'Happy Clients' },
    { value: '98%', label: 'Success Rate' },
    { value: '24/7', label: 'Support Available' },
  ];

  return (
    <section className="benefits">
      <div className="benefits-container">
        <div className="benefits-content">
          <motion.div
            className="content-wrapper"
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <motion.div
              className="header-badge"
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
            >
              Why Choose Us
            </motion.div>

            <h2 className="section-title">
              Your wellness journey
              <br />
              <span className="gradient-text">starts here</span>
            </h2>

            <p className="section-description">
              Join thousands of people who have transformed their lives through
              professional mental health support. Experience the difference that
              personalized care can make.
            </p>

            <div className="stats-grid">
              {stats.map((stat, index) => (
                <motion.div
                  key={index}
                  className="stat-item"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <div className="stat-value">{stat.value}</div>
                  <div className="stat-label">{stat.label}</div>
                </motion.div>
              ))}
            </div>

            <motion.div
              className="cta-group"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <motion.a
                href="/appointment"
                className="btn btn-primary"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Book Your First Session
                <ArrowRight size={18} strokeWidth={2} />
              </motion.a>
              <motion.a
                href="/know_more"
                className="btn btn-ghost"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Learn More
              </motion.a>
            </motion.div>
          </motion.div>
        </div>

        <motion.div
          className="benefits-visual"
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="visual-wrapper">
            <motion.div
              className="visual-ring ring-1"
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: 20,
                repeat: Infinity,
                ease: 'linear',
              }}
            />
            <motion.div
              className="visual-ring ring-2"
              animate={{
                rotate: -360,
              }}
              transition={{
                duration: 25,
                repeat: Infinity,
                ease: 'linear',
              }}
            />
            <motion.div
              className="visual-ring ring-3"
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: 30,
                repeat: Infinity,
                ease: 'linear',
              }}
            />

            <div className="visual-center">
              <motion.div
                className="center-content"
                animate={{
                  scale: [1, 1.05, 1],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
              >
                <div className="center-icon">✨</div>
                <div className="center-text">Your Journey</div>
              </motion.div>
            </div>

            <motion.div
              className="floating-badge badge-1"
              animate={{
                y: [0, -15, 0],
                rotate: [0, 5, 0],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            >
              <span className="badge-emoji">💙</span>
              <span className="badge-text">Mindfulness</span>
            </motion.div>

            <motion.div
              className="floating-badge badge-2"
              animate={{
                y: [0, -20, 0],
                rotate: [0, -5, 0],
              }}
              transition={{
                duration: 5,
                repeat: Infinity,
                ease: 'easeInOut',
                delay: 1,
              }}
            >
              <span className="badge-emoji">🌟</span>
              <span className="badge-text">Growth</span>
            </motion.div>

            <motion.div
              className="floating-badge badge-3"
              animate={{
                y: [0, -10, 0],
                rotate: [0, 3, 0],
              }}
              transition={{
                duration: 3.5,
                repeat: Infinity,
                ease: 'easeInOut',
                delay: 0.5,
              }}
            >
              <span className="badge-emoji">🎯</span>
              <span className="badge-text">Goals</span>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

export default Benefits;
