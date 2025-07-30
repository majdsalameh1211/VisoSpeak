import React, { useState, useEffect } from "react";
import "../design/HomePage.css";
import logo from "../assets/logo_lips.png";
import flowDiagram from "../assets/flow-diagram.png";
import lipnet from "../assets/lipnet_arch.png";
import visualfrontend from "../assets/visual_arch.png";
import trasformer_arch from "../assets/transformer_arch.png";
import { Link } from "react-router-dom";




const transformerImages = [visualfrontend, trasformer_arch];

const HomePage = () => {
  const [scrollY, setScrollY] = useState(0);
  
  const [paused, setPaused] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (paused) return; // pause on hover
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % transformerImages.length);
    }, 3000); // 3 seconds per slide
    return () => clearInterval(interval);
  }, [paused]);

  const currentImage = transformerImages[currentIndex];
  
  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="homepage">
      {/* Subtle Background Pattern */}
      <div className="background-pattern"></div>

      {/* Hero Section */}
      <section className="hero-section">
        {/* Logo Background with Parallax */}
        <div 
          className="hero-logo-bg"
          style={{
            backgroundImage: `url(${logo})`,
            transform: `translateY(${scrollY * 0.3}px)`
          }}
        ></div>

        {/* Hero Content */}
        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-icon">⚡</span>
            Advanced AI Lip Reading Technology
          </div>
          <h1 className="hero-title">VisoSpeak</h1>
          <p className="hero-subtitle">
            Optimizing Lip-Reading Accuracy through Advanced Data Pipelines and Automated Video Processing
          </p>
          <div className="scroll-indicator">
            <div className="chevron-down"></div>
          </div>
        </div>
      </section>

      {/* Why It Matters */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Why VisoSpeak Matters</h2>
            <div className="title-underline"></div>
          </div>
          
          <div className="features-grid">
            <div className="feature-card accent-blue">
              <div className="feature-icon">🎤</div>
              <h3>Silent Communication</h3>
              <p>Bridge communication gaps in noisy environments where traditional speech recognition fails.</p>
            </div>
            <div className="feature-card accent-purple">
              <div className="feature-icon">👥</div>
              <h3>Accessibility Focus</h3>
              <p>Empowering deaf and hard-of-hearing individuals with advanced lip reading technology.</p>
            </div>
            <div className="feature-card accent-green">
              <div className="feature-icon">🧠</div>
              <h3>Universal Solution</h3>
              <p>Works in any situation - from crowded spaces to silent environments.</p>
            </div>
          </div>

          <div className="highlight-box">
            <p>
              Traditional speech recognition systems fail in noisy places, silent environments, or for people who are deaf or hard of hearing. 
              <span className="highlight-text"> VisoSpeak fills this critical gap</span> with AI-powered lip reading technology that works anywhere, anytime.
            </p>
          </div>
        </div>
      </section>

      {/* Solution Overview */}
      <section className="section section-alt">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Our Solution</h2>
            <div className="title-underline"></div>
          </div>

          <div className="solution-content">
            {/* Flow Diagram */}
            <div className="diagram-container">
              <div className="diagram-glow"></div>
              <img
                src={flowDiagram}
                alt="VisoSpeak Workflow Diagram"
                className="flow-diagram"
              />
            </div>

            {/* Solution Description */}
            <div className="solution-description">
              <div className="description-header">
                <p className="intro-text">
                  <strong>Our intelligent pipeline processes video through advanced AI models:</strong>
                </p>
              </div>

              <div className="models-grid">
                <div className="model-card lipnet-model">
                  <div className="model-header">
                    <div className="model-indicator"></div>
                    <h3>LipNet Model</h3>
                  </div>
                  <p>
                    Direct end-to-end processing that transforms video input straight into predicted sentences. 
                    Fast, efficient, and perfect for real-time applications with known vocabulary.
                  </p>
                </div>
                
                <div className="model-card transformer-model">
                  <div className="model-header">
                    <div className="model-indicator"></div>
                    <h3>Transformer-Based Model</h3>
                  </div>
                  <p>
                    Advanced multi-stage approach: generates viseme sequences, processes through Word NLP and Sentence NLP layers. 
                    Handles unseen vocabulary and provides superior accuracy.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

   {/* Models Comparison */}
<section className="section">
  <div className="container">
    <div className="section-header">
      <h2 className="section-title">Two-Model Approach</h2>
      <div className="title-underline"></div>
      <p className="section-subtitle">
        Our system leverages two complementary models trained on different datasets and optimized for distinct use cases.
      </p>
    </div>

<div className="comparison-grid">

  {/* LipNet Model Card */}
  <Link to="/LipNetEndToEnd" className="comparison-card lipnet-card">
    <div className="card-header">
      <div className="card-icon">⚡</div>
      <h3>LipNet Model</h3>
    </div>
    <p className="text-gray-300 text-lg mb-4">
      LipNet is an end-to-end visual speech recognition model that converts lip movements directly into sentences. 
      It uses <strong>3D convolutions</strong> and <strong>bidirectional GRUs</strong> with a <strong>CTC decoder</strong>.
    </p>
    <p className="text-gray-400 text-base mb-6">
      <strong>Training Dataset:</strong> Grid Corpus — 1,000 videos preprocessed into mouth-region frames.
    </p>

    <div className="architecture-images mt-4">
      <img
        src={lipnet}
        alt="LipNet Architecture"
        className="architecture-img shadow-md"
      />
    </div>
  </Link>

  {/* Transformer Model Card */}
  <Link to="/TransformerEndToEnd" className="comparison-card transformer-card">
    <div className="card-header">
      <div className="card-icon">🧠</div>
      <h3>Transformer-Viseme Model</h3>
    </div>
    <p className="text-gray-300 text-lg mb-4">
      The Transformer-based model predicts <strong>viseme sequences</strong> (visual phonemes) instead of characters.
      It combines a <strong>3D CNN + 2D ResNet</strong> visual frontend with a <strong>Transformer encoder-decoder</strong>.
    </p>
    <p className="text-gray-400 text-base mb-6">
      <strong>Training Dataset:</strong> LRS2 Dataset — 80,000 preprocessed videos for open vocabulary recognition.
    </p>

    <div
      className="architecture-images mt-4 relative rounded-lg shadow-md overflow-hidden"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      <img
        src={transformerImages[currentIndex]}
        alt="Transformer Architecture"
        className="architecture-img transition-opacity duration-700 ease-in-out shadow-md"
      />
    </div>
  </Link>

</div>

  </div>
</section>



      {/* Technologies */}
      <section className="section section-alt">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Technologies Used</h2>
            <div className="title-underline"></div>
            <p className="section-subtitle">
              Powered by cutting-edge AI frameworks and tools
            </p>
          </div>

          <div className="tech-grid">
            <div className="tech-badge">
              <span className="tech-icon">🔥</span>
              <span>PyTorch</span>
            </div>
            <div className="tech-badge">
              <span className="tech-icon">🧠</span>
              <span>TensorFlow</span>
            </div>
            <div className="tech-badge">
              <span className="tech-icon">📹</span>
              <span>Mediapipe</span>
            </div>
            <div className="tech-badge">
              <span className="tech-icon">⚡</span>
              <span>GPT-4 API</span>
            </div>
          </div>
        </div>
      </section>

      {/* Results */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Key Results</h2>
            <div className="title-underline"></div>
          </div>

          <div className="results-grid">
            <div className="result-card">
              <div className="result-icon">🏆</div>
              <h3>Word Recognition</h3>
              <p>Successfully recognized individual words and complete sentences from silent videos</p>
            </div>
            
            <div className="result-card">
              <div className="result-icon">📏</div>
              <h3>Word Boundaries Recognition</h3>
              <p>Accurately identified word boundaries and segmentation in continuous speech</p>
            </div>
            
            <div className="result-card">
              <div className="result-icon">⚡</div>
              <h3>High Performance</h3>
              <p>Efficient processing without crashes, even under high load</p>
            </div>
            
            <div className="result-card">
              <div className="result-icon">✅</div>
              <h3>User Validated</h3>
              <p>Validated by deaf and hard-of-hearing users for accessibility</p>
            </div>
          </div>
        </div>
      </section>

      {/* Authors & Advisor Section */}
      <section className="section authors-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Authors & Advisor</h2>
            <div className="title-underline"></div>
          </div>
          
          <div className="authors-content">
            <div className="authors-info">
              <h3>Project Authors</h3>
              <p className="authors-names">Majd Salameh & Morad Asakli</p>
            </div>
            <div className="advisor-info">
              <h4>Project Advisor</h4>
              <p className="advisor-name">Mr. Ilya Zeldner</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;