function transformDate(dateString: string): string {
  // Parse the date string into a Date object
  const dateObject = new Date(dateString);

  // Format the Date object into the desired output
const formattedDate = dateObject.toLocaleString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
});

  return formattedDate;
}

export { transformDate };