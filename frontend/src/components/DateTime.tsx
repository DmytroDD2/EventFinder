const DateTime = () => {
    const formattedDate = new Date().toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false, // Set to true for 12-hour format
    });
  
    return <strong>{formattedDate}</strong>

  };
  
  export default DateTime;