import React from "react";
import { ArrowLeft, CheckCircle, Users, Tag, MessageCircle } from "lucide-react";
import { useScrollAnimation } from "../hooks/useScrollAnimation";

const ProductDetail = ({ product, onBackToProducts, relatedFAQs = [], companyFAQs = [] }) => {
  const [mainRef, isMainVisible] = useScrollAnimation({
    threshold: 0.1,
    delay: 100,
  });

  const [sidebarRef, isSidebarVisible] = useScrollAnimation({
    threshold: 0.1,
    delay: 200,
  });

  if (!product) {
    return (
      <div className="no-results animate-fade-in">
        <h3>Product not found</h3>
        <p>The requested product could not be found.</p>
      </div>
    );
  }

  return (
    <div className="product-detail">
      <div className="product-detail-content">
        <div
          ref={mainRef}
          className={`product-detail-main ${
            isMainVisible ? "animate-slide-up" : "animate-slide-down"
          }`}
        >
          <div className="product-description-section">
            <h2>Description</h2>
            <p className="product-description-full">{product.description}</p>
          </div>

          <div className="product-features-section">
            <h2 className="icon-text-container">
              <CheckCircle size={24} className="icon" />
              Features
            </h2>
            <div className="features-grid">
              {product.features.map((feature, index) => (
                <FeatureItem key={index} feature={feature} index={index} />
              ))}
            </div>
          </div>

          <div className="product-audience-section">
            <h2 className="icon-text-container">
              <Users size={24} className="icon" />
              Target Audience
            </h2>
            <div className="audience-grid">
              {product.targetAudience.map((audience, index) => (
                <AudienceItem key={index} audience={audience} index={index} />
              ))}
            </div>
          </div>

          {/* Related FAQs Section */}
          {(relatedFAQs.length > 0 || companyFAQs.length > 0) && (
            <div className="product-faqs-section">
              <h2 className="icon-text-container">
                <MessageCircle size={24} className="icon" />
                Related FAQs
              </h2>
              <div className="related-faqs">
                {relatedFAQs.length > 0 && (
                  <div className="faq-group">
                    <h3>Product-Specific FAQs</h3>
                    {relatedFAQs.map((faq, index) => (
                      <RelatedFAQItem key={faq.id || index} faq={faq} />
                    ))}
                  </div>
                )}
                {companyFAQs.length > 0 && (
                  <div className="faq-group">
                    <h3>Company-Related FAQs</h3>
                    {companyFAQs.map((faq, index) => (
                      <RelatedFAQItem key={faq.id || index} faq={faq} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div
          ref={sidebarRef}
          className={`product-detail-sidebar ${
            isSidebarVisible ? "animate-slide-up" : "animate-slide-down"
          }`}
        >
          <div className="product-info-card">
            <h3>Product Information</h3>
            <div className="info-item">
              <span className="info-label">Category:</span>
              <span className="info-value">{product.category}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Company:</span>
              <span className="info-value">{product.company}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Features:</span>
              <span className="info-value">{product.features.length}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Target Audiences:</span>
              <span className="info-value">
                {product.targetAudience.length}
              </span>
            </div>
          </div>

          {product.pricing && (
            <div className="product-pricing-card">
              <h3>Pricing</h3>
              <div className="pricing-info">
                <div className="pricing-model">{product.pricing.model}</div>
                {product.pricing.startingPrice && (
                  <div className="pricing-price">
                    Starting from {product.pricing.currency}{" "}
                    {product.pricing.startingPrice}
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="product-actions">
            <button className="contact-button">Contact Company</button>
            <button className="learn-more-button">Learn More</button>
          </div>
        </div>
      </div>
    </div>
  );
};

const FeatureItem = ({ feature, index }) => {
  const [itemRef, isVisible] = useScrollAnimation({
    threshold: 0.1,
    delay: index * 25,
    triggerOnce: true,
  });

  return (
    <div
      ref={itemRef}
      className={`feature-item-full icon-text-container ${
        isVisible ? "animate-fade-in" : "animate-fade-out"
      }`}
    >
      <CheckCircle size={16} className="icon" />
      <span>{feature}</span>
    </div>
  );
};

const AudienceItem = ({ audience, index }) => {
  const [itemRef, isVisible] = useScrollAnimation({
    threshold: 0.1,
    delay: index * 25,
    triggerOnce: true,
  });

  return (
    <div
      ref={itemRef}
      className={`audience-item-full icon-text-container ${
        isVisible ? "animate-fade-in" : "animate-fade-out"
      }`}
    >
      <Users size={16} className="icon" />
      <span>{audience}</span>
    </div>
  );
};

const RelatedFAQItem = ({ faq }) => {
  const [itemRef, isVisible] = useScrollAnimation({
    threshold: 0.1,
    delay: 100,
    triggerOnce: true,
  });

  return (
    <div
      ref={itemRef}
      className={`related-faq-item ${
        isVisible ? "animate-fade-in" : "animate-fade-out"
      }`}
    >
      <div className="faq-question">
        <h4>{faq.question}</h4>
        <p className="faq-answer">{faq.answer}</p>
      </div>
      {faq.keywords && faq.keywords.length > 0 && (
        <div className="faq-keywords">
          {faq.keywords.map((keyword, index) => (
            <span key={index} className="faq-keyword">
              {keyword}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductDetail;
