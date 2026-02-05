const express = require('express');
const cors = require('cors');
require('dotenv').config();
const nodemailer = require('nodemailer');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('../')); // Serve static files from parent directory

// Configure email transporter
const transporter = nodemailer.createTransport({
  service: 'gmail', // or your email service
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
});

// Test email endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

// Submit booking endpoint
app.post('/api/bookings/submit', async (req, res) => {
  try {
    const { name, email, phone, checkin, checkout, nights, basePrice, tax, total, paymentMethod } = req.body;

    // Validate required fields
    if (!name || !email || !phone || !checkin || !checkout) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Prepare email content
    const mailOptions = {
      from: process.env.EMAIL_USER,
      to: email,
      subject: 'Urban Oasis Booking Confirmation',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f9f9f9; padding: 20px; border-radius: 8px;">
          <div style="background: #fff; padding: 30px; border-radius: 8px;">
            <h2 style="color: #8B4513; margin-bottom: 20px;">Booking Confirmation</h2>
            
            <p>Dear <strong>${name}</strong>,</p>
            <p>Thank you for booking with Urban Oasis! Your reservation has been confirmed. Here are your booking details:</p>
            
            <div style="background: #f0f0f0; padding: 20px; border-radius: 6px; margin: 20px 0;">
              <h3 style="color: #333; margin-top: 0;">Order Summary</h3>
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="padding: 8px 0; color: #666;"><strong>Check-in Date:</strong></td>
                  <td style="padding: 8px 0; color: #333; text-align: right;">${checkin}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; color: #666;"><strong>Check-out Date:</strong></td>
                  <td style="padding: 8px 0; color: #333; text-align: right;">${checkout}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; color: #666;"><strong>Total Nights:</strong></td>
                  <td style="padding: 8px 0; color: #333; text-align: right;">${nights}</td>
                </tr>
                <tr style="border-top: 1px solid #ddd; border-bottom: 1px solid #ddd;">
                  <td style="padding: 8px 0; color: #666;"><strong>Base Price:</strong></td>
                  <td style="padding: 8px 0; color: #333; text-align: right;">$${basePrice}</td>
                </tr>
                <tr style="border-bottom: 2px solid #8B4513;">
                  <td style="padding: 8px 0; color: #666;"><strong>Tax (4%):</strong></td>
                  <td style="padding: 8px 0; color: #333; text-align: right;">$${tax}</td>
                </tr>
                <tr>
                  <td style="padding: 12px 0; font-size: 18px; font-weight: bold; color: #8B4513;"><strong>Total Amount:</strong></td>
                  <td style="padding: 12px 0; font-size: 18px; font-weight: bold; color: #8B4513; text-align: right;">$${total}</td>
                </tr>
              </table>
            </div>

            <div style="background: #f0f0f0; padding: 20px; border-radius: 6px; margin: 20px 0;">
              <h3 style="color: #333; margin-top: 0;">Payment Details</h3>
              <p><strong>Payment Method:</strong> ${paymentMethod === 'bank' ? 'Direct Bank Transfer' : paymentMethod === 'card' ? 'Credit/Debit Card' : 'Pay on Arrival'}</p>
              ${paymentMethod === 'bank' ? `
                <p><strong>Company:</strong> Urban Oasis Ltd.</p>
                <p><strong>Bank Account:</strong> xxxxxxxx</p>
                <p><strong>IBAN:</strong> GB00EXAMP00012345678</p>
                <p style="color: #666; font-size: 14px;">Please transfer the total amount and save your receipt for reference.</p>
              ` : paymentMethod === 'card' ? `
                <p style="color: #666; font-size: 14px;">We will contact you to securely take your card details or provide a secure payment link.</p>
              ` : `
                <p style="color: #666; font-size: 14px;">Please be ready to pay in cash or card at check-in.</p>
              `}
            </div>

            <div style="background: #f0f7ff; border-left: 4px solid #8B4513; padding: 15px; margin: 20px 0;">
              <p style="color: #555; margin: 0; font-size: 14px;"><i class="fas fa-info-circle"></i> <strong>Important:</strong> Free cancellation up to 48 hours before check-in.</p>
            </div>

            <p style="color: #666; font-size: 14px;">Your confirmation details have been recorded. If you need to make any changes, please contact us at:</p>
            <p style="color: #8B4513; font-weight: bold;">
              📧 hello@urbanoasis.com<br>
              📞 +1 (254) 555-1234
            </p>

            <p style="color: #666; font-size: 12px; margin-top: 30px; text-align: center;">
              Thank you for choosing Urban Oasis!<br>
              <strong>Urban Oasis — Killeen, TX</strong>
            </p>
          </div>
        </div>
      `
    };

    // Also send a copy to admin
    const adminMailOptions = {
      from: process.env.EMAIL_USER,
      to: process.env.ADMIN_EMAIL || 'hello@urbanoasis.com',
      subject: `New Booking: ${name} (${checkin} - ${checkout})`,
      html: `
        <h2>New Booking Received</h2>
        <p><strong>Guest Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Phone:</strong> ${phone}</p>
        <p><strong>Check-in:</strong> ${checkin}</p>
        <p><strong>Check-out:</strong> ${checkout}</p>
        <p><strong>Nights:</strong> ${nights}</p>
        <p><strong>Total Amount:</strong> $${total}</p>
        <p><strong>Payment Method:</strong> ${paymentMethod}</p>
      `
    };

    // Send emails
    await transporter.sendMail(mailOptions);
    await transporter.sendMail(adminMailOptions);

    res.json({ success: true, message: 'Booking confirmed and email sent!' });
  } catch (error) {
    console.error('Error submitting booking:', error);
    res.status(500).json({ error: 'Failed to submit booking', details: error.message });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
