document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault()

  const email = document.getElementById('email').value
  const password = document.getElementById('password').value

  try {
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    })

    const data = await response.json()

    if (data.message === 'Logged in') {
      window.location.href = '/'
    } else {
      alert('Ошибка входа')
    }
  } catch (error) {
    console.error('Error:', error)
    alert('Произошла ошибка при входе')
  }
})
