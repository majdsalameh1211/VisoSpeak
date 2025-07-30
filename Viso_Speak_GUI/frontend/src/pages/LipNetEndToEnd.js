import React, { useState, useEffect, useRef } from 'react';
import '../design/TransformerEndToEnd.css'; // Reuse same style
import { Link } from "react-router-dom";

const LipNetEndToEnd = () => {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [videos, setVideos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [predictionData, setPredictionData] = useState(null);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [isPredicting, setIsPredicting] = useState(false);
  const [progressText, setProgressText] = useState('');
  const previewVideoRef = useRef(null);
  const progressIntervalRef = useRef(null);

  // ===== Poll backend progress =====
  const pollProgress = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/prediction-progress');
      if (res.ok) {
        const data = await res.json();
        setLoadingProgress(data.progress);
        setProgressText(data.message);

        if (data.progress >= 100 || data.status === 'error') {
          clearInterval(progressIntervalRef.current);
          progressIntervalRef.current = null;
        }
      }
    } catch (err) {
      console.error('Error polling progress:', err);
    }
  };

  const startPolling = () => {
    if (progressIntervalRef.current) clearInterval(progressIntervalRef.current);
    progressIntervalRef.current = setInterval(pollProgress, 200);
  };

  const stopPolling = () => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
      progressIntervalRef.current = null;
    }
  };

  // ===== Handle predict =====
  const handlePredict = async () => {
    if (!selectedVideo) {
      alert("Select a video first.");
      return;
    }

    setIsPredicting(true);
    setLoadingProgress(0);
    setPredictionData(null);
    setProgressText('Starting prediction...');

    startPolling();

    try {
      const response = await fetch('http://127.0.0.1:5000/run-lipnet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_name: selectedVideo.filename }),
      });

      const data = await response.json();

      if (data.status === "success") {
        setPredictionData({
          prediction: data.prediction,
          original: data.original,
        });
        setProgressText('Prediction completed successfully!');
        setLoadingProgress(100);
      } else {
        alert("Error:\n" + data.error);
        setProgressText('Prediction failed');
      }
    } catch (err) {
      alert("Error connecting to backend: " + err.message);
      setProgressText('Connection error');
    } finally {
      stopPolling();
      setTimeout(() => {
        setIsPredicting(false);
        setLoadingProgress(0);
        setProgressText('');
      }, 2000);
    }
  };

  useEffect(() => () => stopPolling(), []);

  // ===== Load videos (simple static for now) =====
  useEffect(() => {
    const videoFiles = [
      "bbal8p.mp4", "bbbf8p.mp4", "bbaf2n.mp4", "bbbf9a.mp4"
    ];

    const videoData = videoFiles.map((filename, index) => ({
      id: index + 1,
      filename,
      path: `/GRID/${filename}`,
      label: filename.replace(".mp4", "").toUpperCase(),
    }));

    setVideos(videoData);
    if (videoData.length > 0) setSelectedVideo(videoData[0]);
    setIsLoading(false);
  }, []);

  const handleVideoSelect = (video) => {
    setSelectedVideo(video);
    if (previewVideoRef.current) previewVideoRef.current.load();
  };

  if (isLoading) {
    return (
      <div className="transformer-page">
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="transformer-page">
      <div className="background-pattern"></div>

      <div className="back-button-top">
        <Link to="/" className="back-btn-top">
          ← Back to Home
        </Link>
      </div>

      <div className="title-section-centered">
        <h2 className="page-title">LipNet End-to-End Prediction</h2>
        <div className="title-underline"></div>
      </div>

      <div className="content-container">
        <div className="content-grid">
          {/* Video List */}
          <div className="video-list">
            <div className="video-list-container">
              <h3 className="section-title">Select Video</h3>
              <div className="thumbnails-container">
                {videos.map((video) => (
                  <div
                    key={video.id}
                    onClick={() => !isPredicting && handleVideoSelect(video)}
                    className={`video-thumbnail ${selectedVideo?.id === video.id ? 'selected' : ''} ${isPredicting ? 'disabled' : ''}`}
                  >
                    <div className="thumbnail-wrapper">
                      <video
                        src={video.path}
                        className="thumbnail-video"
                        muted
                        preload="metadata"
                        playsInline
                      />
                      <div className="video-fallback">
                        <div className="fallback-content">
                          <div className="fallback-icon">🎬</div>
                          <div className="fallback-text">{video.filename}</div>
                        </div>
                      </div>
                    </div>
                    <div className="video-label">{video.label}</div>
                    <div className="video-filename">{video.filename}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Video Preview */}
          <div className="video-preview">
            <div className="preview-container">
              <h3 className="section-title">Video Preview</h3>

              {selectedVideo ? (
                <div className="preview-content">
                  <div className="video-player-wrapper">
                    <video
                      ref={previewVideoRef}
                      key={`preview-${selectedVideo.id}`}
                      src={selectedVideo.path}
                      controls
                      className="preview-video"
                      playsInline
                      preload="metadata"
                    />
                  </div>

                  <div className="video-info">
                    <h4 className="video-title">{selectedVideo.label}</h4>
                    <p className="video-description">{selectedVideo.filename}</p>
                  </div>

                  <div className="button-row">
                    <button 
                      className={`predict-btn ${isPredicting ? 'predicting' : ''}`}
                      onClick={handlePredict}
                      disabled={isPredicting}
                    >
                      {isPredicting ? (
                        <>
                          <div className="button-spinner"></div>
                          Processing...
                        </>
                      ) : (
                        'Predict'
                      )}
                    </button>
                    <button
                      className="predict-btn reload-btn"
                      onClick={() => {
                        if (previewVideoRef.current) previewVideoRef.current.load();
                      }}
                      disabled={isPredicting}
                    >
                      Reload Video
                    </button>
                  </div>

                  {/* Progress bar */}
                  {isPredicting && (
                    <div className="progress-section">
                      <div className="progress-bar-container">
                        <div
                          className="progress-bar-fill"
                          style={{ width: `${loadingProgress}%` }}
                        ></div>
                      </div>
                      <div className="progress-info">
                        <span className="progress-text">{progressText}</span>
                        <span className="progress-percentage">{loadingProgress}%</span>
                      </div>
                    </div>
                  )}

                  {/* Prediction Results */}
                  {predictionData && !isPredicting && (
                    <div className="prediction-results">
                      <div className="results-header">
                        <h4 className="results-title">
                          <span className="results-icon">🎯</span>
                          Prediction Results
                        </h4>
                      </div>
                      <div className="results-content">
                        <div className="result-section predicted">
                          <div className="section-header">
                          
                            <strong className="section-title">Predicted Text</strong>
                          </div>
                          <p>{predictionData.prediction}</p>
                        </div>
                        <div className="result-section ground-truth">
                          <div className="section-header">
                            
                            <strong className="section-title">Original Text</strong>
                          </div>
                          <p>{predictionData.original}</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="no-selection">
                  <p className="no-selection-text">Select a video to preview</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LipNetEndToEnd;
