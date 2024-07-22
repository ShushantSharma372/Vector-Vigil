document.getElementById('contactForm').addEventListener('submit', function(event) {
//   event.preventDefault();
  
//   const data = {
//       firstName: document.getElementById('firstName').value,
//       lastName: document.getElementById('lastName').value,
//       email: document.getElementById('email').value,
//       website: document.getElementById('website').value,
//       region: document.getElementById('region').value
//   };

//   console.log('Form data:', data); // Add this line to log form data to console
  
//   fetch('/alert', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(data),
//   })
//   .then(response => response.json())
//   .then(data => {
//       alert('Form submitted successfully!');
//       console.log('Success:', data);
//   })
//   .catch((error) => {
//       console.error('Error:', error);
//   });
// });
