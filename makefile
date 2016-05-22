#Main compiler
CC := g++

SRCDIR := src
BUILDDIR := build
TARGET := ./build/test

SRCEXT := cc
#SOURCES := $(shell find $(SRCDIR) -type f -name *.$(SRCEXT))

SOURCES := $(shell find $(SRCDIR) -type f -name landmark.$(SRCEXT))
SOURCES += /usr/include/dlib/all/source.cpp

OBJECTS := $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.$(SRCEXT)=.o))
CFLAGS := -ggdb -O3 -Wall -msse2 -DDLIB_JPEG_SUPPORT
LIB := -lpthread -lX11 -ljpeg
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
	@echo " $(RM) -r $(BUILDDIR) $(TARGET)"; $(RM) -r $(BUILDDIR) $(TARGET)
	
.PHONY: clean