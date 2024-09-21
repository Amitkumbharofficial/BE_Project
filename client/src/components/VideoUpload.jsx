import React, { useState } from 'react';

const VideoUpload = () => {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [processedVideo, setProcessedVideo] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVideoChange = (event) => {
    setSelectedVideo(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!selectedVideo) {
      alert('Please select a video file first.');
      return;
    }

    setLoading(true);
    
    try {
        const formData = new FormData();
        formData.append('video', selectedVideo);
      const response = await fetch('http://localhost:5000/process-video', {
        method: 'POST',
        body: formData,
      });
      console.log("send");
      
      if (response.ok) {
        console.log("ok");
        
        const result = await response.blob();
        const videoUrl = URL.createObjectURL(result);  
        setProcessedVideo(videoUrl);  
      } else {
        console.error('Error processing video.');
      }
    } catch (error) {
      console.error('Error uploading video:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Video Upload & Processing</h1>

      <div className="mb-4">
        <input type="file" accept="video/*" onChange={handleVideoChange} className="border p-2" />
      </div>

      {selectedVideo && (
        <div className="mb-4">
          <h2 className="text-xl font-semibold mb-2">Selected Video:</h2>
          <video
            src={URL.createObjectURL(selectedVideo)}
            controls
            className="max-w-full h-auto border"
          />
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        {loading ? 'Processing...' : 'Submit Video'}
      </button>

      {processedVideo && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">Processed Video:</h2>
          <video src={processedVideo} controls className="max-w-full h-auto border" />
        </div>
      )}
    </div>
  );
};

export default VideoUpload;
