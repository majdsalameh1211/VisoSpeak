import React, { useState, useEffect, useRef } from 'react';
import '../design/TransformerEndToEnd.css';
import { Link } from "react-router-dom";

const TransformerEndToEnd = () => {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [videos, setVideos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [videoLoadErrors, setVideoLoadErrors] = useState({});
  const [videoSupport, setVideoSupport] = useState({});
  const previewVideoRef = useRef(null);

  // New states for prediction
  const [predictionData, setPredictionData] = useState(null);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [isPredicting, setIsPredicting] = useState(false);
  const [progressText, setProgressText] = useState('');
  const progressIntervalRef = useRef(null);

  // === Real-time Progress Polling ===
  const pollProgress = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/prediction-progress');
      const data = await response.json();
      
      setLoadingProgress(data.progress);
      setProgressText(data.message);
      
      // Stop polling when prediction is complete or on error
      if (data.progress >= 100 || data.status === 'error') {
        if (progressIntervalRef.current) {
          clearInterval(progressIntervalRef.current);
          progressIntervalRef.current = null;
        }
      }
    } catch (error) {
      console.error('Error polling progress:', error);
    }
  };

  // === Start Progress Polling ===
  const startProgressPolling = () => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
    }
    
    // Poll every 200ms for smooth progress updates
    progressIntervalRef.current = setInterval(pollProgress, 200);
  };

  // === Stop Progress Polling ===
  const stopProgressPolling = () => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
      progressIntervalRef.current = null;
    }
  };

  // === Enhanced Predict Handler ===
  const handlePredict = async () => {
    if (!selectedVideo) {
      alert("Please select a video first.");
      return;
    }

    setIsPredicting(true);
    setLoadingProgress(0);
    setPredictionData(null);
    setProgressText('Starting prediction...');

    // Start polling for progress updates
    startProgressPolling();

    try {
      const response = await fetch('http://127.0.0.1:5000/run-transformer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_name: selectedVideo.filename }),
      });

      const data = await response.json();

      if (data.status === "success") {
        setPredictionData(data);
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
      // Stop polling and reset after a delay
      stopProgressPolling();
      setTimeout(() => {
        setIsPredicting(false);
        setLoadingProgress(0);
        setProgressText('');
      }, 2000); // Show completion state for 2 seconds
    }
  };

  // === Cleanup progress polling on unmount ===
  useEffect(() => {
    return () => {
      stopProgressPolling();
    };
  }, []);

  // === Check video codec support ===
  useEffect(() => {
    const checkVideoSupport = () => {
      const video = document.createElement('video');
      const support = {
        mp4: video.canPlayType('video/mp4; codecs="avc1.42E01E"') !== '',
        webm: video.canPlayType('video/webm; codecs="vp8, vorbis"') !== '',
        ogg: video.canPlayType('video/ogg; codecs="theora"') !== '',
        h264: video.canPlayType('video/mp4; codecs="avc1.42E01E, mp4a.40.2"') !== '',
        h265: video.canPlayType('video/mp4; codecs="hev1.1.6.L93.B0"') !== ''
      };
      setVideoSupport(support);
      console.log('Video codec support:', support);
    };

    checkVideoSupport();
  }, []);

  // === Load available videos ===
  useEffect(() => {
    const videoFiles = [
      "00001.mp4", "00002.mp4", "00003.mp4", "00005.mp4", "00006.mp4",
      "00009.mp4", "00010.mp4", "00011.mp4", "00012.mp4", "00013.mp4",
      "00016.mp4", "00019.mp4", "00020.mp4", "00021.mp4",
      "00022.mp4", "00025.mp4", "00027.mp4", "00028.mp4"
    ];

    const videoData = videoFiles.map((filename, index) => ({
      id: index + 1,
      filename,
      path: `/LRS2/${filename}`,
      label: filename.replace(".mp4", "").toUpperCase(),
    }));

    setVideos(videoData);
    setSelectedVideo(videoData[0]);
    setIsLoading(false);
  }, []);

  const handleVideoSelect = (video) => {
    setSelectedVideo(video);
    if (previewVideoRef.current) {
      previewVideoRef.current.load();
    }
  };

  const handleVideoError = (videoId, error) => {
    console.error(`Video ${videoId} failed to load:`, error);
    setVideoLoadErrors(prev => ({
      ...prev,
      [videoId]: true
    }));
  };

  const handleVideoLoadSuccess = (videoId) => {
    setVideoLoadErrors(prev => ({
      ...prev,
      [videoId]: false
    }));
  };

  const handleVideoLoadStart = (videoId) => {
    console.log(`Video ${videoId} started loading`);
  };

  const handleVideoCanPlay = (videoId, element) => {
    console.log(`Video ${videoId} can play`);
    if (element) {
      element.style.display = 'block';
      const fallback = element.nextElementSibling;
      if (fallback && fallback.classList.contains('video-fallback')) {
        fallback.style.display = 'none';
      }
    }
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
      {/* Background */}
      <div className="background-pattern"></div>

      {/* Back Button */}
      <div className="back-button-top">
        <Link to="/" className="back-btn-top">
          ← Back to Home
        </Link>
      </div>

      {/* Title */}
      <div className="title-section-centered">
        <h2 className="page-title">
          Transformer  Vismes ArrayPrediction
        </h2>
        <div className="title-underline"></div>
      </div>

      {/* Codec Warning */}
      {!videoSupport.mp4 && (
        <div className="codec-warning">
          ⚠️ Your browser may not support MP4 video playback. Videos might only play audio.
        </div>
      )}

      {/* Content */}
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
                        onLoadStart={() => handleVideoLoadStart(`thumb-${video.id}`)}
                        onError={(e) => {
                          handleVideoError(video.id, e);
                          e.target.style.display = 'none';
                          e.target.nextElementSibling.style.display = 'flex';
                        }}
                        onLoadedData={() => handleVideoLoadSuccess(video.id)}
                        onCanPlay={(e) => handleVideoCanPlay(`thumb-${video.id}`, e.target)}
                      >
                        <source src={video.path} type="video/mp4; codecs='avc1.42E01E, mp4a.40.2'" />
                        <source src={video.path} type="video/mp4" />
                        Your browser does not support the video tag.
                      </video>
                      <div
                        className="video-fallback"
                        style={{ display: videoLoadErrors[video.id] ? 'flex' : 'none' }}
                      >
                        <div className="fallback-content">
                          <div className="fallback-icon">🎬</div>
                          <div className="fallback-text">{video.filename}</div>
                          <div className="fallback-error">Video not available</div>
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
                      crossOrigin="anonymous"
                      onLoadStart={() => handleVideoLoadStart(`preview-${selectedVideo.id}`)}
                      onError={(e) => {
                        console.error('Preview video error:', e);
                        handleVideoError(`preview-${selectedVideo.id}`, e);
                        e.target.style.display = 'none';
                        e.target.nextElementSibling.style.display = 'flex';
                      }}
                      onLoadedData={() => handleVideoLoadSuccess(`preview-${selectedVideo.id}`)}
                      onCanPlay={(e) => handleVideoCanPlay(`preview-${selectedVideo.id}`, e.target)}
                    >
                      <source src={selectedVideo.path} type="video/mp4; codecs='avc1.42E01E, mp4a.40.2'" />
                      <source src={selectedVideo.path} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                    <div
                      className="preview-fallback"
                      style={{
                        display: videoLoadErrors[`preview-${selectedVideo.id}`] ? 'flex' : 'none'
                      }}
                    >
                      <div className="preview-fallback-content">
                        <div className="preview-fallback-icon">🎬</div>
                        <div className="preview-fallback-title">Video not found or unsupported format</div>
                        <div className="preview-fallback-filename">{selectedVideo.filename}</div>
                      </div>
                    </div>
                  </div>

                  {/* Video Info */}
                  <div className="video-info">
                    <h4 className="video-title">{selectedVideo.label}</h4>
                    <p className="video-description">{selectedVideo.filename}</p>
                  </div>

                  {/* Buttons */}
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
                        if (previewVideoRef.current) {
                          previewVideoRef.current.load();
                          setVideoLoadErrors(prev => ({
                            ...prev,
                            [`preview-${selectedVideo.id}`]: false
                          }));
                        }
                      }}
                      disabled={isPredicting}
                    >
                      Reload Video
                    </button>
                  </div>

                  {/* Real-time Progress Bar */}
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
                      <div className="progress-details">
                        <div className="progress-stage">
                          <span className={`stage-indicator ${loadingProgress >= 10 ? 'completed' : 'pending'}`}>●</span>
                          <span className="stage-text">Video Loading</span>
                        </div>
                        <div className="progress-stage">
                          <span className={`stage-indicator ${loadingProgress >= 30 ? 'completed' : loadingProgress >= 10 ? 'active' : 'pending'}`}>●</span>
                          <span className="stage-text">Frame Processing</span>
                        </div>
                        <div className="progress-stage">
                          <span className={`stage-indicator ${loadingProgress >= 55 ? 'completed' : loadingProgress >= 30 ? 'active' : 'pending'}`}>●</span>
                          <span className="stage-text">Model Loading</span>
                        </div>
                        <div className="progress-stage">
                          <span className={`stage-indicator ${loadingProgress >= 85 ? 'completed' : loadingProgress >= 55 ? 'active' : 'pending'}`}>●</span>
                          <span className="stage-text">Prediction</span>
                        </div>
                        <div className="progress-stage">
                          <span className={`stage-indicator ${loadingProgress >= 100 ? 'completed' : loadingProgress >= 85 ? 'active' : 'pending'}`}>●</span>
                          <span className="stage-text">Finalizing</span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Enhanced Prediction Results */}
                  {predictionData && !isPredicting && (
                    <div className="prediction-results">
                      <div className="results-header">
                        <h4 className="results-title">
                          <span className="results-icon">🎯</span>
                          Prediction Results
                        </h4>
                        <div className="results-badges">
                          <div className="accuracy-badge viseme">
                            <span className="badge-label">Viseme</span>
                            <span className="badge-value">{predictionData.viseme_match_percent}%</span>
                          </div>
                          <div className="accuracy-badge boundary">
                            <span className="badge-label">Boundary</span>
                            <span className="badge-value">{predictionData.boundary_match_percent}%</span>
                          </div>
                        </div>
                      </div>

                      <div className="results-content">
                        <div className="result-section predicted">
                          <div className="section-header">
                            
                            <strong className="section-title">Predicted Tokens</strong>
                          </div>
                          <div className="tokens-container">
                            <div className="tokens-wrapper">
                              {predictionData.pred_tokens.map((token, index) => (
                                <span key={index} className="token predicted-token">
                                  {token}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>

                        <div className="result-section ground-truth">
                          <div className="section-header">
                           
                            <strong className="section-title">Ground Truth Tokens</strong>
                          </div>
                          <div className="tokens-container">
                            <div className="tokens-wrapper">
                              {predictionData.true_tokens.map((token, index) => (
                                <span key={index} className="token truth-token">
                                  {token}
                                </span>
                              ))}
                            </div>
                          </div>
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

export default TransformerEndToEnd;