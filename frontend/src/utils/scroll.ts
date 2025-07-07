const scrollToTopWithOffset = (wrapper: string) => {
  const scrollContainer = document.querySelector(wrapper);
  
  const scrollOptions = {
    top: 0 ,
    behavior: 'smooth' as ScrollBehavior,
  };

  window.scrollTo(scrollOptions);

  if (scrollContainer instanceof HTMLElement) {
    scrollContainer.scrollTo(scrollOptions);
  }
};
export default scrollToTopWithOffset;