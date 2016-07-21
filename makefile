#Main compiler
CC := g++

SRCDIR := src
BUILDDIR := build
TARGET := build/emo

SRCEXT := cc
SOURCES := $(shell find $(SRCDIR) -type f -name *.$(SRCEXT))

#Link dlib's source.cpp
SOURCES += /usr/include/dlib/all/source.cpp

OBJECTS := $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.$(SRCEXT)=.o))
CFLAGS := -O3 -Wall -mavx -std=c++11 -DDLIB_JPEG_SUPPORT `pkg-config opencv --cflags`
LIB := -lpthread -lX11 -ljpeg `pkg-config opencv --libs` $(SRCDIR)/libsvm.a

#Link path to dlib include files
INC := -I /usr/include/

#Main target
$(TARGET): $(OBJECTS)
	@echo " Linking..."
	@echo " $(CC) $^ -o $(TARGET) $(LIB)"; $(CC) $^ -o 	$(TARGET) $(LIB)

#Object files
$(BUILDDIR)/%.o: $(SRCDIR)/%.$(SRCEXT)
	@echo " Build object..."
	@mkdir -p $(BUILDDIR)
	@echo " $(CC) $(CFLAGS) $(INC) -c -o $@ $<"; $(CC) $(CFLAGS) $(INC) -c -o $@ $<

#Remove generated files
clean:
	@echo " Cleaning..."
	@echo " $(RM) -r $(BUILDDIR) $(TARGET)"; $(RM) -r $(TARGET)
	
.PHONY: clean