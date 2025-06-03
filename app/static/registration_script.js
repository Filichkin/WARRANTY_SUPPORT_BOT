document.getElementById('registrationForm').addEventListener('submit', async (e) => {
    e.preventDefault()
  
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value
    const first_name = document.getElementById('firstname').value
    const last_name = document.getElementById('lastname').value
    const dealer_code = document.getElementById('dealercode').value
    const phone_number = document.getElementById('phone').value
  
    try {
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, phone_number, first_name, last_name, dealer_code }),
        credentials: 'include',
      })
  
      const data = await response.json()
  
      if (data.message === 'Successeful registration!') {
        window.location.href = '/auth/login/'
      } else {
        alert('Ошибка регистрации')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Произошла ошибка при регистрации')
    }
  })