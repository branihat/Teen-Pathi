# Render Deployment Guide

This guide will help you deploy your betting application to Render with MongoDB.

## Prerequisites

1. **GitHub Repository**: Push your code to a GitHub repository
2. **Render Account**: Create a free account at [render.com](https://render.com)
3. **MongoDB Database**: Your MongoDB connection string (already configured)

## Step 1: Prepare Your Repository

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

## Step 2: Deploy Backend on Render

### Option A: Using Render Blueprint (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file and create services automatically
5. Set environment variables in the Render dashboard:
   - `MONGODB_URL`: Your MongoDB connection string
   - `STRIPE_SECRET_KEY`: Your Stripe secret key
   - `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key
   - `STRIPE_WEBHOOK_SECRET`: Your Stripe webhook secret

### Option B: Manual Setup

1. **Create Web Service**:
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `betting-app-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Health Check Path**: `/health`

2. **Set Environment Variables**:
   - `MONGODB_URL`: Your MongoDB connection string
   - `DATABASE_NAME`: `betting_db`
   - `SECRET_KEY`: Generate a secure random string
   - `DEBUG`: `false`
   - `CORS_ORIGINS`: Will be updated after frontend deployment
   - `STRIPE_SECRET_KEY`: Your Stripe secret key
   - `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key
   - `STRIPE_WEBHOOK_SECRET`: Your Stripe webhook secret

## Step 3: Deploy Frontend on Render

1. **Create Static Site**:
   - Go to Render Dashboard
   - Click "New" → "Static Site"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `betting-app-frontend`
     - **Build Command**: `cd frontend && flutter pub get && flutter build web --release`
     - **Publish Directory**: `frontend/build/web`

2. **Update Backend CORS Settings**:
   - Go to your backend service settings
   - Update `CORS_ORIGINS` environment variable with your frontend URL
   - Example: `https://betting-app-frontend.onrender.com`

## Step 4: Set Up Redis (Optional)

If you need Redis for caching:

1. **Add Redis Service**:
   - Go to Render Dashboard
   - Click "New" → "Redis"
   - Choose a plan (Free tier available)
   - Get the Redis URL from the service details

2. **Update Backend Environment**:
   - Add `REDIS_URL` environment variable to your backend service
   - Use the Redis URL provided by Render

## Step 5: Configure MongoDB

Your MongoDB is already configured with the connection string:
```
mongodb+srv://emcfileshare:jZsHNMxwoPZhkOgn@cluster0.i0ldkeu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

Make sure to:
1. **Whitelist Render IPs** in your MongoDB Atlas network settings
2. **Create database indexes** if needed (handled automatically by Beanie)

## Step 6: Test Your Deployment

1. **Check Backend Health**:
   ```bash
   curl https://your-backend-url.onrender.com/health
   ```

2. **Check Frontend**:
   - Visit your frontend URL
   - Test user registration and login
   - Verify API calls work

## Step 7: Set Up Custom Domain (Optional)

1. **Add Custom Domain**:
   - Go to your service settings
   - Add your custom domain
   - Configure DNS records as instructed

2. **Update CORS Settings**:
   - Update `CORS_ORIGINS` with your custom domain

## Environment Variables Summary

For your backend service, set these environment variables:

```
MONGODB_URL=mongodb+srv://emcfileshare:jZsHNMxwoPZhkOgn@cluster0.i0ldkeu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DATABASE_NAME=betting_db
SECRET_KEY=your-super-secret-key-here
DEBUG=false
CORS_ORIGINS=https://your-frontend-url.onrender.com
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **Database Connection Issues**:
   - Check MongoDB connection string
   - Verify network access in MongoDB Atlas
   - Check environment variable names

3. **CORS Issues**:
   - Update `CORS_ORIGINS` with correct frontend URL
   - Include both HTTP and HTTPS if needed

4. **Frontend Build Issues**:
   - Ensure Flutter is properly configured
   - Check for missing dependencies
   - Verify build command

### Logs and Monitoring:

- **Backend Logs**: Available in Render dashboard under your web service
- **Build Logs**: Check during deployment for build issues
- **Runtime Logs**: Monitor application errors and performance

## Production Considerations

1. **Security**:
   - Use strong secret keys
   - Enable HTTPS (automatic with Render)
   - Implement rate limiting
   - Set up proper authentication

2. **Performance**:
   - Use Redis for caching
   - Optimize database queries
   - Consider CDN for static assets

3. **Monitoring**:
   - Set up health checks
   - Monitor application performance
   - Set up error tracking

## Support

If you encounter issues:
1. Check Render documentation
2. Review application logs
3. Verify environment variables
4. Test MongoDB connection
5. Check CORS configuration

## Next Steps

After successful deployment:
1. Set up monitoring and logging
2. Configure backup strategies
3. Set up CI/CD pipelines
4. Add SSL certificates for custom domains
5. Implement production security measures
